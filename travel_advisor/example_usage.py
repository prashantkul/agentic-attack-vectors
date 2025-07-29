"""
Example usage of the Memory-Enhanced Travel Advisor Agent using ADK

This example demonstrates how to use the travel advisor agent with Vertex AI Memory Bank
for long-term memory across conversations using the Agent Development Kit (ADK).
"""

import asyncio
import os
from dotenv import load_dotenv
from travel_advisor.agent import create_memory_enabled_runner
from travel_advisor.memory_bank import create_memory_service

# Load environment variables from .env file
load_dotenv()

async def example_with_runner():
    """
    Example using ADK Runner with memory capabilities.
    """
    print("🧠 ADK Memory-Enhanced Travel Advisor Example")
    print("=" * 50)
    
    try:
        # Create memory-enabled runner
        runner = create_memory_enabled_runner("travel_advisor_demo")
        
        # Create session for user
        user_id = "john_doe"
        session = await runner.session_service.create_session(
            app_name="travel_advisor_demo",
            user_id=user_id
        )
        
        print(f"📝 Created session: {session.session_id}")
        
        # First conversation - establish preferences
        print("\n👤 User: I'm looking for budget-friendly destinations in Europe for hiking")
        
        # Run conversation turn
        response1 = await runner.run_turn(
            session=session,
            input="I'm looking for budget-friendly destinations in Europe for hiking"
        )
        print(f"🤖 Agent: {response1.content}")
        
        # Add session to memory for learning
        if runner.memory_service:
            await runner.memory_service.add_session_to_memory(session)
            print("💾 Added conversation to memory bank")
        
        # Second conversation - should use memory
        print("\n👤 User: What about mountain destinations for next summer?")
        
        response2 = await runner.run_turn(
            session=session,
            input="What about mountain destinations for next summer?"
        )
        print(f"🤖 Agent: {response2.content}")
        
        # Add session to memory again
        if runner.memory_service:
            await runner.memory_service.add_session_to_memory(session)
            print("💾 Updated memory bank with new conversation")
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("This is expected if you haven't configured Google Cloud credentials")

async def example_agent_engine_setup():
    """
    Example showing how to check Agent Engine setup.
    """
    print("\n🔧 Agent Engine Setup Status")
    print("=" * 40)
    
    try:
        # Check if AGENT_ENGINE_ID is set
        agent_engine_id = os.getenv("AGENT_ENGINE_ID")
        
        if agent_engine_id:
            print(f"✅ AGENT_ENGINE_ID is set: {agent_engine_id}")
            
            # Test memory service creation
            try:
                memory_service = create_memory_service()
                print(f"✅ Memory service created successfully")
            except Exception as e:
                print(f"❌ Memory service creation failed: {e}")
        else:
            print("❌ AGENT_ENGINE_ID not set")
            print()
            print("🔧 To create an Agent Engine:")
            print("   python setup_agent_engine.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have set GOOGLE_CLOUD_PROJECT environment variable")

def setup_instructions():
    """
    Print setup instructions for using ADK Memory Bank.
    """
    print("\n⚙️  ADK Memory Bank Setup Instructions")
    print("=" * 40)
    print("1. Set up Google Cloud Project with Vertex AI enabled")
    print("2. Enable required APIs:")
    print("   - Vertex AI API")
    print("   - Agent Engine API")
    print("3. Create a .env file from .env.example:")
    print("   cp .env.example .env")
    print("   # Edit .env with your actual values")
    print("4. Key environment variables:")
    print("   GOOGLE_GENAI_USE_VERTEXAI=1")
    print("   GOOGLE_CLOUD_PROJECT=your-project-id")
    print("   GOOGLE_CLOUD_LOCATION=us-central1  # Required for Memory Bank")
    print("   AGENT_ENGINE_ID=your-agent-engine-id")
    print("5. Set up authentication:")
    print("   - Service account key file OR")
    print("   - Application Default Credentials (gcloud auth application-default login)")
    print("6. Ensure appropriate IAM permissions:")
    print("   - Vertex AI User")
    print("   - AI Platform Developer")
    print("7. Install dependencies: pip install -r requirements.txt")
    print("8. Create Agent Engine (one-time setup):")
    print("   python setup_agent_engine.py")

async def main():
    """
    Main example runner.
    """
    setup_instructions()
    
    print("\n🚀 Running ADK Memory Examples...")
    
    # Check if environment variables are set
    if not os.getenv("GOOGLE_CLOUD_PROJECT") or not os.getenv("AGENT_ENGINE_ID"):
        print("\n⚠️  Warning: Environment variables not set. Examples will use in-memory fallback.")
        print("Set GOOGLE_CLOUD_PROJECT and AGENT_ENGINE_ID for full memory functionality.")
    
    try:
        await example_with_runner()
        await example_agent_engine_setup()
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("This is expected if you haven't set up Google Cloud credentials.")

if __name__ == "__main__":
    asyncio.run(main())