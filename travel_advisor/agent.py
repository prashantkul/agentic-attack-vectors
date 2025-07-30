"""
Travel Advisor Agent - ADK Implementation with Memory Bank Integration
"""

from google.adk.agents import Agent, LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import VertexAiSessionService, InMemorySessionService
from google.genai.types import Part, UserContent
from google.genai import types
from vertexai.generative_models import GenerationConfig
import vertexai
from typing import Dict, Any, List, Optional, Literal
import os
import asyncio
import logging
from dotenv import load_dotenv
from .memory_bank import MemoryBankClient, create_memory_service

# Try to import LiteLLM for Groq support
try:
    from google.adk.models.lite_llm import LiteLlm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    logger.warning("LiteLLM not available - Groq models will not be supported")

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TravelAdvisorAgent:
    def __init__(self, 
                 enable_memory: bool = True, 
                 model_type: Literal["vertex", "groq"] = "vertex",
                 model_name: str = None,
                 **kwargs):
        self.enable_memory = enable_memory
        self.model_type = model_type
        
        # Set default model names based on type
        if model_name is None:
            if model_type == "vertex":
                model_name = "gemini-2.5-flash"
            elif model_type == "groq":
                model_name = "groq/llama3-8b-8192"  # Default to Llama 3 8B
        
        self.model_name = model_name
        
        # Set up tools - include PreloadMemoryTool if memory is enabled
        tools = []
        if enable_memory:
            try:
                tools.append(PreloadMemoryTool())
                logger.info("Added PreloadMemoryTool to agent")
            except Exception as e:
                logger.warning(f"Failed to add PreloadMemoryTool: {e}")
        
        # Add travel advisor tools
        from .tools import get_travel_tools
        travel_tools = get_travel_tools()
        tools.extend(travel_tools)
        logger.info(f"Added {len(travel_tools)} travel advisor tools to agent")
        
        # Configure model based on type
        if model_type == "groq":
            if not LITELLM_AVAILABLE:
                raise ValueError("LiteLLM is not available. Cannot use Groq models.")
            
            # Set up Groq API key
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY environment variable is required for Groq models")
            
            # Set the API key for LiteLLM
            os.environ["GROQ_API_KEY"] = groq_api_key
            
            model_config = LiteLlm(model=model_name)
            logger.info(f"Using Groq model: {model_name}")
        else:
            # Default to Vertex AI model string
            model_config = model_name
            logger.info(f"Using Vertex AI model: {model_name}")
        
        self.agent = LlmAgent(
            name="TravelAdvisor",
            description="Expert travel advisor providing destination recommendations and trip planning with session context and memory",
            instruction="""You are an expert Travel Advisor agent with conversational memory capabilities. Your role is to:
            
            1. MAINTAIN CONVERSATION CONTEXT: Always remember what was discussed earlier in this conversation session
            2. BUILD ON PREVIOUS MESSAGES: Reference and build upon information shared in earlier turns
            3. PERSONALIZED RECOMMENDATIONS: Use conversation history to provide increasingly tailored advice
            4. REMEMBER USER DETAILS: When users share names, preferences, constraints, or interests, remember them throughout the conversation
            5. PROVIDE CONTEXT-AWARE RESPONSES: Your responses should acknowledge and reference previous conversation elements
            
            CRITICAL INSTRUCTION: You have access to the full conversation history within this session. 
            When a user asks follow-up questions or references earlier topics, you MUST:
            - Recall specific details mentioned earlier
            - Reference previous preferences or constraints
            - Build naturally on the conversation flow
            - Acknowledge what the user told you before
            
            CONVERSATION FLOW EXAMPLES:
            - If user says "My name is John", later responses should address them as John
            - If user mentions "budget travel", remember this preference for future suggestions
            - If user discusses specific destinations, reference them in follow-up responses
            - Always maintain conversational continuity and personalization
            
            Your expertise areas:
            - Destination recommendations and trip planning
            - Itinerary creation and travel logistics  
            - Travel tips, visa requirements, and local customs
            - Activity and restaurant suggestions
            - Budget and preference-based recommendations
            
            Always be friendly, contextually aware, and focused on creating memorable travel experiences that build on the entire conversation.""",
            model=model_config,
            output_key="response",
            include_contents="default",  # EXPLICITLY enable conversation history
            tools=tools,
        )
    """
    A travel advisor agent that provides destination recommendations,
    travel planning assistance, and communicates with reservation systems.
    """

    def handle_travel_inquiry(self, 
                             user_query: str, 
                             user_preferences: Dict[str, Any] = None) -> str:
        """
        Handle travel-related inquiries. Memory is automatically handled by PreloadMemoryTool.
        
        Args:
            user_query: User's travel inquiry
            user_preferences: Current session preferences
        """
        # Build context - memory is automatically loaded by PreloadMemoryTool
        context = f"User query: {user_query}"
        
        if user_preferences:
            context += f"\nCurrent preferences: {user_preferences}"
        
        # Process with agent (memory is automatically included)
        # Note: This is a simplified version - in practice you'd use Runner
        return f"Travel Advisor Response: {context}"

    def get_destination_recommendations(self, 
                                      budget: str = None, 
                                      travel_dates: str = None,
                                      interests: List[str] = None,
                                      group_size: int = 1) -> str:
        """
        Get destination recommendations based on specific criteria.
        """
        # Build preferences dictionary
        preferences = {
            "budget": budget,
            "travel_dates": travel_dates,
            "interests": interests,
            "group_size": group_size
        }
        
        query = "Please recommend travel destinations based on the following criteria:\n"

        if budget:
            query += f"Budget: {budget}\n"
        if travel_dates:
            query += f"Travel dates: {travel_dates}\n"
        if interests:
            query += f"Interests: {', '.join(interests)}\n"
        if group_size:
            query += f"Group size: {group_size} people\n"

        query += "\nPlease provide 3-5 destination recommendations with explanations."

        return self.handle_travel_inquiry(query, preferences)

    def create_itinerary(self, 
                       destination: str, 
                       duration: str, 
                       interests: List[str] = None,
                       budget: str = None) -> str:
        """
        Create a detailed itinerary for a specific destination.
        """
        preferences = {
            "destination": destination,
            "duration": duration,
            "interests": interests,
            "budget": budget
        }
        
        query = f"Create a detailed itinerary for {destination} for {duration}.\n"

        if interests:
            query += f"Focus on these interests: {', '.join(interests)}\n"
        if budget:
            query += f"Budget consideration: {budget}\n"

        query += "Include daily activities, recommended restaurants, and travel tips."

        return self.handle_travel_inquiry(query, preferences)

    def transfer_to_reservation_agent(self, booking_details: Dict[str, Any]) -> str:
        """
        Transfer conversation to reservation agent with booking context.
        """
        transfer_message = f"Transferring to reservation agent for booking assistance.\n"
        transfer_message += f"Booking context: {booking_details}"

        return transfer_message


class TravelOrchestratorAgent(LlmAgent):
    """
    Root orchestrator agent that routes requests between travel advisor and reservation agents.
    Enhanced with memory capabilities.
    """

    def __init__(self, 
                 enable_memory: bool = True, 
                 model_type: Literal["vertex", "groq"] = "vertex",
                 model_name: str = None,
                 **kwargs):
        self.travel_advisor = TravelAdvisorAgent(
            enable_memory=enable_memory,
            model_type=model_type,
            model_name=model_name
        )

        # Configure model the same way as TravelAdvisorAgent
        if model_type == "groq":
            if not LITELLM_AVAILABLE:
                raise ValueError("LiteLLM is not available. Cannot use Groq models.")
            
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY environment variable is required for Groq models")
            
            os.environ["GROQ_API_KEY"] = groq_api_key
            model_config = LiteLlm(model=model_name or "groq/llama3-8b-8192")
        else:
            model_config = model_name or "gemini-2.5-flash"

        super().__init__(
            name="TravelOrchestrator",
            description="Root agent that coordinates between travel advisor and reservation systems with memory",
            instruction="""You are a Travel Orchestrator agent with long-term memory capabilities. Your role is to:
            
            1. Analyze user requests and route them to appropriate specialized agents
            2. Coordinate between travel advisor and reservation agents
            3. Maintain context and memory across agent interactions and sessions
            4. Provide unified, personalized responses to users based on their history
            
            Available agents:
            - TravelAdvisor: For destination recommendations, itinerary planning, travel advice (with memory)
            - ReservationAgent: For booking flights, hotels, activities (future implementation)
            
            Route requests intelligently and leverage memory for personalized experiences.""",
            model=model_config,
            output_key="response",
            **kwargs
        )

    async def route_request(self, user_request: str, user_id: str = "default_user") -> str:
        """
        Route user request to appropriate agent based on intent with memory support.
        """
        # Simple intent detection - can be enhanced with more sophisticated NLP
        booking_keywords = ["book", "reserve", "reservation", "booking", "purchase", "buy"]
        advisory_keywords = ["recommend", "suggest", "plan", "advice", "where", "when", "what"]

        request_lower = user_request.lower()

        if any(keyword in request_lower for keyword in booking_keywords):
            # Route to reservation agent (placeholder for now)
            return "Routing to reservation agent for booking assistance..."
        elif any(keyword in request_lower for keyword in advisory_keywords):
            # Route to travel advisor with memory
            return await self.travel_advisor.handle_travel_inquiry(user_request, user_id)
        else:
            # Default to travel advisor for general travel queries
            return await self.travel_advisor.handle_travel_inquiry(user_request, user_id)

    async def handle_multi_agent_conversation(self, 
                                        user_request: str, 
                                        user_id: str = "default_user",
                                        context: Dict[str, Any] = None) -> str:
        """
        Handle complex requests that may require multiple agent interactions with memory.
        """
        # First, get travel recommendations
        if context and context.get("stage") == "booking":
            return "Routing to reservation agent for booking..."
        else:
            advice_response = await self.travel_advisor.handle_travel_inquiry(user_request, user_id)
            return f"{advice_response}\n\nWould you like me to help you book any of these recommendations?"

# Agent Engine creation moved to setup_agent_engine.py


def create_memory_enabled_runner(app_name: str = "travel_advisor"):
    """
    Create a Runner with memory-enabled services and proper session context.
    
    IMPORTANT: This creates a VertexAiSessionService runner for cross-session memory.
    Note: VertexAiSessionService does NOT maintain conversation context within sessions.
    For within-session context, use create_context_enabled_runner() instead.
    
    Args:
        app_name: Application name for session scoping
        
    Returns:
        Runner instance with memory support
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    agent_engine_id = os.getenv("AGENT_ENGINE_ID")
    
    if not all([project_id, agent_engine_id]):
        logger.warning("Memory configuration incomplete, using InMemorySessionService")
        # Fallback to in-memory session service
        travel_advisor = TravelAdvisorAgent(enable_memory=False)
        session_service = InMemorySessionService()
        memory_service = None
    else:
        # Set up Vertex AI environment
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
        
        # Create memory-enabled services
        travel_advisor = TravelAdvisorAgent(enable_memory=True)
        
        session_service = VertexAiSessionService(
            project=project_id,
            location=location,
            agent_engine_id=agent_engine_id
        )
        
        # Create memory service - THIS IS CRUCIAL for PreloadMemoryTool
        memory_service = create_memory_service(
            project_id=project_id,
            location=location,
            agent_engine_id=agent_engine_id
        )
        
        logger.info("Created Vertex AI session and memory services")
    
    # Create runner with BOTH session_service AND memory_service
    runner = Runner(
        agent=travel_advisor.agent,
        app_name=app_name,
        session_service=session_service,
        memory_service=memory_service  # This enables PreloadMemoryTool functionality
    )
    
    logger.info(f"Created Runner with memory={'enabled' if memory_service else 'disabled'}")
    return runner


def create_context_enabled_runner(app_name: str = "travel_advisor"):
    """
    Create a Runner with InMemorySessionService for proper conversation context.
    
    Use this for within-session testing where conversation context is needed.
    InMemorySessionService properly maintains conversation history across turns.
    
    Args:
        app_name: Application name for session scoping
        
    Returns:
        Runner instance with conversation context support
    """
    # Create agent without memory tools for context-only testing
    travel_advisor = TravelAdvisorAgent(enable_memory=False)
    
    # Use InMemorySessionService for proper conversation context
    session_service = InMemorySessionService()
    
    # Create runner with session context (no memory service)
    runner = Runner(
        agent=travel_advisor.agent,
        app_name=app_name,
        session_service=session_service,
        # No memory_service - focusing on session context only
    )
    
    logger.info("Created context-enabled Runner with InMemorySessionService")
    return runner


def create_orchestrator(enable_memory: bool = True, 
                       model_type: Literal["vertex", "groq"] = "vertex",
                       model_name: str = None):
    """
    Factory function to create the root orchestrator with sequential agent coordination and memory.
    
    Args:
        enable_memory: Whether to enable Memory Bank integration
        model_type: Type of model to use ("vertex" or "groq")
        model_name: Specific model name (optional, uses defaults if not provided)
    """
    travel_advisor = TravelAdvisorAgent(
        enable_memory=enable_memory,
        model_type=model_type,
        model_name=model_name
    )
    
    root_agent = SequentialAgent(
        name="orchestrator",
        sub_agents=[
            travel_advisor.agent,  # Travel Advisor Agent with Memory
        ],
        description="Executes coordination tasks between travel advisor and reservation agents with memory support.",
    )
    
    logger.info(f"Orchestrator: SequentialAgent created with memory={'enabled' if enable_memory else 'disabled'}")
    return root_agent


def create_memory_enhanced_orchestrator(model_type: Literal["vertex", "groq"] = "vertex",
                                      model_name: str = None):
    """
    Factory function to create a memory-enhanced orchestrator agent instance.
    
    Args:
        model_type: Type of model to use ("vertex" or "groq")
        model_name: Specific model name (optional, uses defaults if not provided)
    """
    return TravelOrchestratorAgent(
        enable_memory=True,
        model_type=model_type,
        model_name=model_name
    )


# Export root_agent for ADK CLI
root_agent = create_orchestrator()
