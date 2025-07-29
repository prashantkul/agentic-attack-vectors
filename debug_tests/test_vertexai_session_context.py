#!/usr/bin/env python3
"""
Test if VertexAiSessionService maintains conversation context like InMemorySessionService
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from travel_advisor.agent import TravelAdvisorAgent
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.genai import types

# Load environment variables
load_dotenv()

async def test_vertexai_session_context():
    """Test if VertexAiSessionService maintains conversation context."""
    print("🧪 Testing VertexAiSessionService Conversation Context")
    print("=" * 55)
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    agent_engine_id = os.getenv("AGENT_ENGINE_ID")
    
    if not all([project_id, agent_engine_id]):
        print("❌ Missing Vertex AI configuration")
        return False
    
    # Create travel agent (without memory for this test - focus on session context only)
    travel_agent = TravelAdvisorAgent(enable_memory=False)
    
    # Use VertexAiSessionService (the one that didn't work before)
    session_service = VertexAiSessionService(
        project=project_id,
        location=location,
        agent_engine_id=agent_engine_id
    )
    
    # Create runner with VertexAi session service
    runner = Runner(
        app_name="vertexai_session_test",
        agent=travel_agent.agent,
        session_service=session_service
    )
    
    # Create session
    session = await session_service.create_session(
        app_name="vertexai_session_test",
        user_id="test_traveler"
    )
    
    print(f"✅ VertexAi Session created: {session.id}")
    
    # Helper function to send messages
    def send_message(message):
        content = types.Content(parts=[types.Part(text=message)])
        events = list(runner.run(
            user_id="test_traveler",
            session_id=session.id,
            new_message=content
        ))
        return "".join([
            part.text for part in events[-1].content.parts 
            if hasattr(part, 'text') and part.text
        ])
    
    # Test conversation flow - same as our successful InMemory test
    conversations = [
        "Hi, my name is Michael and I'm planning a trip to France",
        "I have a budget of $2500 for the whole trip", 
        "I'm interested in art museums and wine tasting",
        "What's my name and what are my travel preferences?",
        "Based on what I told you, what would you recommend in France?"
    ]
    
    responses = []
    
    for i, message in enumerate(conversations, 1):
        print(f"\n📤 Message {i}:")
        print(f"   User: {message}")
        
        response = send_message(message)
        responses.append(response)
        
        print(f"   Agent: {response[:150]}{'...' if len(response) > 150 else ''}")
        
        # Check for context retention in later messages
        if i >= 4:
            context_indicators = ["michael", "Michael", "$2500", "2500", "budget", "art", "museums", "wine"]
            has_context = any(indicator in response for indicator in context_indicators)
            print(f"   Context retained: {'🟢 YES' if has_context else '🔴 NO'}")
    
    # Final session analysis
    final_session = await session_service.get_session(
        app_name="vertexai_session_test",
        user_id="test_traveler",
        session_id=session.id
    )
    
    print(f"\n📊 Session Analysis:")
    print(f"   Total events: {len(final_session.events)}")
    print(f"   Expected events: 10 (5 user + 5 agent)")
    
    # Detailed context analysis
    response4 = responses[3]  # "What's my name and preferences?"
    response5 = responses[4]  # "What would you recommend?"
    
    name_remembered = "michael" in response4.lower() or "Michael" in response4
    budget_remembered = "$2500" in response4 or "2500" in response4
    interests_remembered = any(word in response4.lower() for word in ["art", "museums", "wine"])
    
    contextual_recommendation = any(word in response5.lower() for word in ["michael", "budget", "art", "museums", "wine", "louvre", "bordeaux"])
    
    print(f"\n📊 Detailed Analysis:")
    print(f"   Name remembered: {'🟢 YES' if name_remembered else '🔴 NO'}")
    print(f"   Budget remembered: {'🟢 YES' if budget_remembered else '🔴 NO'}")
    print(f"   Interests remembered: {'🟢 YES' if interests_remembered else '🔴 NO'}")
    print(f"   Contextual recommendations: {'🟢 YES' if contextual_recommendation else '🔴 NO'}")
    
    overall_success = name_remembered and (budget_remembered or interests_remembered)
    
    return overall_success

async def main():
    """Main test function."""
    try:
        result = await test_vertexai_session_context()
        if result:
            print("\n🎉 SUCCESS: VertexAiSessionService maintains conversation context!")
            print("   ✅ Both InMemory and VertexAi session services work for context")
            print("   ✅ Ready for comprehensive memory poisoning tests")
        else:
            print("\n💥 FAILED: VertexAiSessionService not maintaining conversation context")
            print("   ❌ Will need to use InMemory for within-session tests")
            print("   ❌ VertexAi can only be used for cross-session memory tests")
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())