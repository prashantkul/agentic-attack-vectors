#!/usr/bin/env python3
"""
Test script to verify Memory Bank connectivity and functionality.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from travel_advisor.memory_bank import create_memory_service
from travel_advisor.agent import create_memory_enabled_runner
from google.genai import types

# Load environment variables
load_dotenv()

async def test_memory_service_creation():
    """Test if we can create a memory service."""
    print("🧪 Testing Memory Service Creation")
    print("=" * 40)
    
    try:
        # Check required environment variables
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        agent_engine_id = os.getenv("AGENT_ENGINE_ID")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        print(f"📋 Configuration:")
        print(f"   Project ID: {project_id}")
        print(f"   Agent Engine ID: {agent_engine_id}")
        print(f"   Location: {location}")
        print()
        
        if not project_id:
            print("❌ GOOGLE_CLOUD_PROJECT not set")
            return False
            
        if not agent_engine_id:
            print("❌ AGENT_ENGINE_ID not set")
            return False
        
        # Try to create memory service
        print("🔧 Creating memory service...")
        memory_service = create_memory_service(
            project_id=project_id,
            location=location,
            agent_engine_id=agent_engine_id
        )
        
        print("✅ Memory service created successfully!")
        print(f"   Service type: {type(memory_service)}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create memory service: {e}")
        return False

async def test_runner_creation():
    """Test if we can create a memory-enabled runner."""
    print("\n🧪 Testing Memory-Enabled Runner Creation")
    print("=" * 45)
    
    try:
        print("🔧 Creating memory-enabled runner...")
        runner = create_memory_enabled_runner("memory_test")
        
        print("✅ Runner created successfully!")
        print(f"   Runner type: {type(runner)}")
        print(f"   Has memory service: {runner.memory_service is not None}")
        print(f"   Session service type: {type(runner.session_service)}")
        print(f"   Runner methods: {[m for m in dir(runner) if not m.startswith('_')]}")
        
        return True, runner
        
    except Exception as e:
        print(f"❌ Failed to create runner: {e}")
        return False, None

async def test_session_creation(runner):
    """Test if we can create a session."""
    print("\n🧪 Testing Session Creation")
    print("=" * 30)
    
    try:
        print("🔧 Creating session...")
        session = await runner.session_service.create_session(
            app_name="memory_test",
            user_id="test_user_123"
        )
        
        print("✅ Session created successfully!")
        print(f"   Session type: {type(session)}")
        print(f"   Session attributes: {dir(session)}")
        
        # Get session ID (use 'id' attribute for ADK sessions)
        session_id = session.id
        print(f"   Session ID: {session_id}")
        print(f"   User ID: {getattr(session, 'user_id', 'N/A')}")
        print(f"   App Name: {getattr(session, 'app_name', 'N/A')}")
        
        return True, session
        
    except Exception as e:
        print(f"❌ Failed to create session: {e}")
        return False, None

async def test_conversation_turn(runner, session):
    """Test running a conversation turn with correct ADK API."""
    print("\n🧪 Testing Conversation Turn")
    print("=" * 32)
    
    try:
        print("🔧 Running conversation turn...")
        test_input = "I'm looking for budget travel destinations in Europe"
        
        # Create Content object from string input
        content = types.Content(parts=[types.Part(text=test_input)])
        
        # Use correct ADK Runner API
        print(f"   Using session ID: {session.id}")
        print(f"   Using user ID: {session.user_id}")
        
        # Run with correct parameters (all keyword-only)
        event_generator = runner.run(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content
        )
        
        # Collect events from the generator
        events = []
        for event in event_generator:
            events.append(event)
            print(f"   Event: {type(event).__name__}")
            if hasattr(event, 'content'):
                print(f"   Content preview: {str(event.content)[:100]}...")
        
        print("✅ Conversation turn completed!")
        print(f"   Input: {test_input}")
        print(f"   Generated {len(events)} events")
        
        return True, events
        
    except Exception as e:
        print(f"❌ Failed to run conversation turn: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def test_memory_storage(runner, session):
    """Test adding session to memory bank."""
    print("\n🧪 Testing Memory Bank Storage")
    print("=" * 35)
    
    try:
        if not runner.memory_service:
            print("⚠️  No memory service available - skipping memory storage test")
            return False
            
        print("🔧 Adding session to memory bank...")
        await runner.memory_service.add_session_to_memory(session)
        
        print("✅ Session added to memory bank successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add session to memory: {e}")
        return False

async def run_all_tests():
    """Run all memory bank tests."""
    print("🚀 Starting Memory Bank Tests")
    print("=" * 50)
    
    # Test 1: Memory service creation
    service_ok = await test_memory_service_creation()
    
    # Test 2: Runner creation
    runner_ok, runner = await test_runner_creation()
    
    if not runner_ok:
        print("\n💥 Cannot proceed with further tests - runner creation failed")
        return
    
    # Test 3: Session creation
    session_ok, session = await test_session_creation(runner)
    
    if not session_ok:
        print("\n💥 Cannot proceed with memory tests - session creation failed")
        return
    
    # Test 4: Conversation turn
    conversation_ok, response = await test_conversation_turn(runner, session)
    
    # Test 5: Memory storage (only if we have memory service)
    memory_ok = await test_memory_storage(runner, session)
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Memory Service Creation: {'✅' if service_ok else '❌'}")
    print(f"Runner Creation: {'✅' if runner_ok else '❌'}")
    print(f"Session Creation: {'✅' if session_ok else '❌'}")
    print(f"Conversation Turn: {'✅' if conversation_ok else '❌'}")
    print(f"Memory Storage: {'✅' if memory_ok else '❌'}")
    
    overall_success = all([service_ok, runner_ok, session_ok, conversation_ok])
    memory_success = memory_ok
    
    print(f"\n🎯 Overall Status:")
    if overall_success and memory_success:
        print("🟢 All tests passed! Memory Bank is fully functional.")
    elif overall_success:
        print("🟡 Basic functionality works, but memory storage needs configuration.")
        print("   Check your AGENT_ENGINE_ID and Google Cloud credentials.")
    else:
        print("🔴 Some tests failed. Check your configuration and credentials.")

if __name__ == "__main__":
    asyncio.run(run_all_tests())