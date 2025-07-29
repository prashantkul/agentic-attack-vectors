#!/usr/bin/env python3
"""
Simple test to check memory bank imports and basic functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_imports():
    """Test if we can import the memory bank modules."""
    print("🧪 Testing Imports")
    print("=" * 20)
    
    try:
        from travel_advisor.memory_bank import create_memory_service, MemoryBankClient
        print("✅ memory_bank imports successful")
    except Exception as e:
        print(f"❌ memory_bank import failed: {e}")
        return False
        
    try:
        from travel_advisor.agent import create_memory_enabled_runner
        print("✅ agent imports successful")
    except Exception as e:
        print(f"❌ agent import failed: {e}")
        return False
        
    try:
        from google.adk.memory import VertexAiMemoryBankService
        print("✅ ADK memory import successful")
    except Exception as e:
        print(f"❌ ADK memory import failed: {e}")
        return False
        
    try:
        from google.adk.tools.preload_memory_tool import PreloadMemoryTool
        print("✅ PreloadMemoryTool import successful")
    except Exception as e:
        print(f"❌ PreloadMemoryTool import failed: {e}")
        return False
        
    return True

def test_environment():
    """Test environment variable setup."""
    print("\n🧪 Testing Environment Variables")
    print("=" * 35)
    
    vars_to_check = [
        ("GOOGLE_GENAI_USE_VERTEXAI", os.getenv("GOOGLE_GENAI_USE_VERTEXAI")),
        ("GOOGLE_CLOUD_PROJECT", os.getenv("GOOGLE_CLOUD_PROJECT")),
        ("GOOGLE_CLOUD_LOCATION", os.getenv("GOOGLE_CLOUD_LOCATION")),
        ("AGENT_ENGINE_ID", os.getenv("AGENT_ENGINE_ID")),
    ]
    
    all_good = True
    for var_name, var_value in vars_to_check:
        if var_value:
            print(f"✅ {var_name}: {var_value}")
        else:
            print(f"❌ {var_name}: Not set")
            if var_name in ["GOOGLE_CLOUD_PROJECT", "AGENT_ENGINE_ID"]:
                all_good = False
    
    return all_good

def test_memory_service_creation():
    """Test memory service creation with error handling."""
    print("\n🧪 Testing Memory Service Creation")
    print("=" * 40)
    
    try:
        from travel_advisor.memory_bank import create_memory_service
        
        # Test with missing required parameters (if no env vars)
        if not (os.getenv("GOOGLE_CLOUD_PROJECT") and os.getenv("AGENT_ENGINE_ID")):
            try:
                memory_service = create_memory_service()
                print("❌ Should have failed with missing parameters")
                return False
            except ValueError as e:
                print(f"✅ Correctly failed with missing parameters: {e}")
        else:
            print("✅ Required parameters available via environment variables")
        
        # Test with provided parameters (if available)
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        agent_engine_id = os.getenv("AGENT_ENGINE_ID")
        
        if project_id and agent_engine_id:
            try:
                memory_service = create_memory_service(
                    project_id=project_id,
                    agent_engine_id=agent_engine_id
                )
                print(f"✅ Memory service created: {type(memory_service)}")
                return True
            except Exception as e:
                print(f"⚠️  Memory service creation failed (expected without proper setup): {e}")
                return False
        else:
            print("⚠️  Skipping actual memory service creation - missing env vars")
            return True
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run all simple tests."""
    print("🚀 Running Simple Memory Bank Tests")
    print("=" * 50)
    
    imports_ok = test_imports()
    env_ok = test_environment()
    memory_ok = test_memory_service_creation()
    
    print("\n📊 Simple Test Results")
    print("=" * 25)
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"Environment: {'✅' if env_ok else '❌'}")
    print(f"Memory Service: {'✅' if memory_ok else '❌'}")
    
    if imports_ok and env_ok:
        print("\n🟢 Basic setup looks good!")
        if not env_ok:
            print("💡 Set GOOGLE_CLOUD_PROJECT and AGENT_ENGINE_ID for full functionality")
    else:
        print("\n🔴 Some basic issues found - check imports and environment setup")

if __name__ == "__main__":
    main()