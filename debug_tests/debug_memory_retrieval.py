#!/usr/bin/env python3
"""
Debug script to test memory retrieval with PreloadMemoryTool
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from travel_advisor.agent import TravelAdvisorAgent
from travel_advisor.memory_bank import create_memory_service
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.genai import types

# Load environment variables
load_dotenv()

async def debug_memory_retrieval():
    """Debug the memory retrieval process step by step."""
    print("🔍 DEBUGGING MEMORY RETRIEVAL")
    print("=" * 50)
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    agent_engine_id = os.getenv("AGENT_ENGINE_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not all([project_id, agent_engine_id]):
        print("❌ Missing required environment variables")
        return
    
    # Set up Vertex AI environment
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
    
    print(f"📝 Project: {project_id}")
    print(f"📝 Agent Engine: {agent_engine_id}")
    print(f"📝 Location: {location}")
    
    # Create memory-enabled agent
    print("\n🤖 Creating memory-enabled agent...")
    travel_agent = TravelAdvisorAgent(enable_memory=True)
    print(f"✅ Agent created with {len(travel_agent.agent.tools)} tools")
    
    # Check if PreloadMemoryTool is present
    preload_tool_present = any('PreloadMemoryTool' in str(tool) for tool in travel_agent.agent.tools)
    print(f"🧠 PreloadMemoryTool present: {preload_tool_present}")
    
    # Create services
    session_service = VertexAiSessionService(
        project=project_id,
        location=location,
        agent_engine_id=agent_engine_id
    )
    
    memory_service = create_memory_service(
        project_id=project_id,
        location=location,
        agent_engine_id=agent_engine_id
    )
    
    # Create runner
    runner = Runner(
        app_name="debug_memory",
        agent=travel_agent.agent,
        session_service=session_service,
        memory_service=memory_service
    )
    
    print("✅ Services and runner created")
    
    def send_message(session_id, message):
        content = types.Content(role="user", parts=[types.Part(text=message)])
        events = list(runner.run(
            user_id="debug_user",
            session_id=session_id,
            new_message=content
        ))
        return "".join([
            part.text for part in events[-1].content.parts 
            if hasattr(part, 'text') and part.text
        ])
    
    # Session 1: Store some preference information
    print("\n📤 SESSION 1: Storing preference information")
    session1 = await session_service.create_session(
        app_name="debug_memory",
        user_id="debug_user"
    )
    print(f"   Session ID: {session1.id}")
    
    message1 = "My name is Alice and I love luxury spa resorts with ocean views, budget is $500+ per night"
    print(f"   👤 USER: {message1}")
    
    response1 = send_message(session1.id, message1)
    print(f"   🤖 AGENT: {response1[:200]}...")
    
    # Save session to memory
    print("\n💾 Saving session to memory bank...")
    await memory_service.add_session_to_memory(session1)
    print("⏳ Waiting for memory processing...")
    await asyncio.sleep(15)  # Wait longer for processing
    print("✅ Memory processing complete")
    
    # Session 2: Test memory retrieval
    print("\n📤 SESSION 2: Testing memory retrieval")
    session2 = await session_service.create_session(
        app_name="debug_memory",
        user_id="debug_user"  # Same user ID
    )
    print(f"   Session ID: {session2.id}")
    
    message2 = "What's my name and what kind of hotels do I like?"
    print(f"   👤 USER: {message2}")
    
    response2 = send_message(session2.id, message2)
    print(f"   🤖 AGENT: {response2}")
    
    # Analysis
    print("\n📊 MEMORY RETRIEVAL ANALYSIS:")
    name_remembered = "alice" in response2.lower() or "Alice" in response2
    preferences_remembered = any(word in response2.lower() for word in ["luxury", "spa", "ocean", "$500"])
    
    print(f"   👤 Name remembered: {'✅ YES' if name_remembered else '❌ NO'}")
    print(f"   🏨 Preferences remembered: {'✅ YES' if preferences_remembered else '❌ NO'}")
    
    if name_remembered and preferences_remembered:
        print("🎉 SUCCESS: Memory retrieval working correctly!")
    else:
        print("❌ FAILED: Memory not being retrieved properly")
        print("\nPossible issues:")
        print("1. PreloadMemoryTool not working as expected")
        print("2. Memory needs more time to be indexed")
        print("3. User ID or session configuration issue")
        print("4. Memory service configuration problem")

if __name__ == "__main__":
    asyncio.run(debug_memory_retrieval())