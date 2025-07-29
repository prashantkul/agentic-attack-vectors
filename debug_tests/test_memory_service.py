#!/usr/bin/env python3
"""
Test the corrected VertexAiMemoryBankService setup
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from travel_advisor.memory_bank import create_memory_service
from travel_advisor.agent import TravelAdvisorAgent
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.genai import types

# Load environment variables
load_dotenv()

async def test_memory_service_setup():
    """Test the corrected VertexAiMemoryBankService setup."""
    print("🧪 Testing VertexAiMemoryBankService Setup")
    print("=" * 45)
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    agent_engine_id = os.getenv("AGENT_ENGINE_ID")
    
    print(f"📋 Configuration:")
    print(f"   Project ID: {project_id}")
    print(f"   Location: {location}")
    print(f"   Agent Engine ID: {agent_engine_id}")
    
    if not all([project_id, agent_engine_id]):
        print("❌ Missing required configuration")
        return False
    
    try:
        # Test memory service creation
        print("\n🔧 Creating VertexAiMemoryBankService...")
        memory_service = create_memory_service(
            project_id=project_id,
            location=location,
            agent_engine_id=agent_engine_id
        )
        print("✅ Memory service created successfully")
        
        # Test session service creation
        print("\n🔧 Creating VertexAiSessionService...")
        session_service = VertexAiSessionService(
            project=project_id,
            location=location,
            agent_engine_id=agent_engine_id
        )
        print("✅ Session service created successfully")
        
        # Test agent creation with memory
        print("\n🔧 Creating memory-enabled agent...")
        travel_agent = TravelAdvisorAgent(enable_memory=True)
        print("✅ Memory-enabled agent created successfully")
        
        # Test runner creation
        print("\n🔧 Creating runner with memory service...")
        runner = Runner(
            app_name="memory_test",
            agent=travel_agent.agent,
            session_service=session_service,
            memory_service=memory_service
        )
        print("✅ Runner with memory service created successfully")
        
        # Test session creation
        print("\n🔧 Creating session...")
        session = await session_service.create_session(
            app_name="memory_test",
            user_id="test_user"
        )
        print(f"✅ Session created: {session.id}")
        
        # Test a simple interaction
        print("\n🔧 Testing basic interaction...")
        content = types.Content(parts=[types.Part(text="Hello, I'm planning a trip to Tokyo")])
        
        events = list(runner.run(
            user_id="test_user",
            session_id=session.id,
            new_message=content
        ))
        
        response = "".join([
            part.text for part in events[-1].content.parts 
            if hasattr(part, 'text') and part.text
        ])
        
        print(f"🤖 Agent response: {response[:100]}...")
        
        # Test memory addition
        print("\n🔧 Testing memory addition...")
        if hasattr(memory_service, 'add_session_to_memory'):
            await memory_service.add_session_to_memory(session)
            print("✅ Session added to memory successfully")
        else:
            print("ℹ️  Memory service doesn't have add_session_to_memory method")
        
        print("\n🎉 All memory service tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Memory service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    try:
        result = await test_memory_service_setup()
        if result:
            print("\n✅ Memory service is properly configured")
            print("   Ready for memory poisoning tests with both session and memory context")
        else:
            print("\n❌ Memory service configuration needs fixing")
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())