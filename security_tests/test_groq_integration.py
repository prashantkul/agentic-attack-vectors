#!/usr/bin/env python3
"""
Test script to verify Groq integration with LiteLLM works correctly.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from travel_advisor.agent import TravelAdvisorAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Load environment variables
load_dotenv()

async def test_groq_integration():
    """Test both Vertex AI and Groq models."""
    print("🧪 Testing Groq Integration with LiteLLM")
    print("=" * 50)
    
    # Test 1: Verify Vertex AI still works (baseline)
    print("\n1️⃣ Testing Vertex AI model (baseline):")
    try:
        vertex_agent = TravelAdvisorAgent(
            enable_memory=False,
            model_type="vertex",
            model_name="gemini-2.5-flash"
        )
        print("✅ Vertex AI agent created successfully")
    except Exception as e:
        print(f"❌ Vertex AI agent failed: {e}")
        return
    
    # Test 2: Test Groq model creation
    print("\n2️⃣ Testing Groq model creation:")
    try:
        groq_agent = TravelAdvisorAgent(
            enable_memory=False,
            model_type="groq",
            model_name="groq/llama3-8b-8192"
        )
        print("✅ Groq agent created successfully")
        print(f"   Model: {groq_agent.model_name}")
        print(f"   Type: {groq_agent.model_type}")
    except Exception as e:
        print(f"❌ Groq agent creation failed: {e}")
        return
    
    # Test 3: Test actual conversation with Groq
    print("\n3️⃣ Testing Groq conversation:")
    
    # Check for Groq API key 
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️ GROQ_API_KEY not set - skipping conversation test")
        print("   Please add your Groq API key to .env file to test conversations")
        return
    
    try:
        # Create runner with Groq agent
        session_service = InMemorySessionService()
        runner = Runner(
            app_name="groq_test",
            agent=groq_agent.agent,
            session_service=session_service
        )
        
        # Create session
        session = await session_service.create_session(
            app_name="groq_test",
            user_id="groq_tester"
        )
        
        print("✅ Groq runner and session created")
        
        # Test conversation
        test_message = "Hi! I'm planning a trip to Japan. Can you help me?"
        print(f"\n👤 USER: {test_message}")
        
        content = types.Content(role="user", parts=[types.Part(text=test_message)])
        events = list(runner.run(
            user_id="groq_tester",
            session_id=session.id,
            new_message=content
        ))
        
        response = "".join([
            part.text for part in events[-1].content.parts 
            if hasattr(part, 'text') and part.text
        ])
        
        print(f"🤖 GROQ (Llama 3): {response[:200]}...")
        print("✅ Groq conversation successful!")
        
        # Test context retention
        print("\n4️⃣ Testing Groq context retention:")
        followup = "What did I just ask you about?"
        print(f"👤 USER: {followup}")
        
        content = types.Content(role="user", parts=[types.Part(text=followup)])
        events = list(runner.run(
            user_id="groq_tester",
            session_id=session.id,
            new_message=content
        ))
        
        response2 = "".join([
            part.text for part in events[-1].content.parts 
            if hasattr(part, 'text') and part.text
        ])
        
        print(f"🤖 GROQ (Llama 3): {response2[:200]}...")
        
        # Check if it remembered Japan
        if "japan" in response2.lower() or "trip" in response2.lower():
            print("✅ Context retention working!")
        else:
            print("⚠️ Context retention may not be working")
            
    except Exception as e:
        print(f"❌ Groq conversation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🎉 Groq integration test completed!")
    print("\nAvailable Groq models:")
    print("- groq/llama3-8b-8192 (Llama 3 8B)")
    print("- groq/llama3-70b-8192 (Llama 3 70B)")
    print("- groq/mixtral-8x7b-32768 (Mixtral 8x7B)")
    print("- groq/gemma-7b-it (Gemma 7B)")

async def test_model_comparison():
    """Compare responses between Vertex AI and Groq models."""
    print("\n🔬 Model Comparison Test")
    print("=" * 30)
    
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️ GROQ_API_KEY not set - skipping model comparison")
        return
    
    test_prompt = "Recommend a 3-day itinerary for Tokyo"
    
    # Test with different models
    models_to_test = [
        {"type": "vertex", "name": "gemini-2.5-flash", "label": "Gemini 2.5 Flash"},
        {"type": "groq", "name": "groq/llama3-8b-8192", "label": "Llama 3 8B"},
        {"type": "groq", "name": "groq/llama3-70b-8192", "label": "Llama 3 70B"},
    ]
    
    for model_config in models_to_test:
        print(f"\n🤖 Testing {model_config['label']}:")
        try:
            agent = TravelAdvisorAgent(
                enable_memory=False,
                model_type=model_config["type"],
                model_name=model_config["name"]
            )
            
            session_service = InMemorySessionService()
            runner = Runner(
                app_name="comparison_test",
                agent=agent.agent,
                session_service=session_service
            )
            
            session = await session_service.create_session(
                app_name="comparison_test",
                user_id="comparison_tester"
            )
            
            content = types.Content(role="user", parts=[types.Part(text=test_prompt)])
            events = list(runner.run(
                user_id="comparison_tester",
                session_id=session.id,
                new_message=content
            ))
            
            response = "".join([
                part.text for part in events[-1].content.parts 
                if hasattr(part, 'text') and part.text
            ])
            
            print(f"Response length: {len(response)} characters")
            print(f"Preview: {response[:150]}...")
            print("✅ Success")
            
        except Exception as e:
            print(f"❌ Failed: {e}")

async def main():
    """Main test function."""
    await test_groq_integration()
    await test_model_comparison()

if __name__ == "__main__":
    asyncio.run(main())