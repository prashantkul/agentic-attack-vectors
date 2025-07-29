#!/usr/bin/env python3
"""
Verify that your agent is properly configured for ADK Web with memory.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_adk_web_memory_config():
    """Verify ADK Web memory configuration."""
    print("🔍 Verifying ADK Web Memory Configuration")
    print("=" * 45)
    
    # Check environment variables
    required_vars = {
        "GOOGLE_GENAI_USE_VERTEXAI": os.getenv("GOOGLE_GENAI_USE_VERTEXAI"),
        "GOOGLE_CLOUD_PROJECT": os.getenv("GOOGLE_CLOUD_PROJECT"), 
        "GOOGLE_CLOUD_LOCATION": os.getenv("GOOGLE_CLOUD_LOCATION"),
        "AGENT_ENGINE_ID": os.getenv("AGENT_ENGINE_ID")
    }
    
    print("📋 Environment Variables:")
    all_set = True
    for var, value in required_vars.items():
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: Not set")
            all_set = False
    
    if not all_set:
        print("\n⚠️  Some environment variables are missing!")
        print("   Make sure to set them in your .env file or environment")
        return False
    
    # Check agent configuration
    print("\n🤖 Agent Configuration:")
    try:
        from travel_advisor.agent import create_memory_enabled_runner, root_agent
        
        # Test runner creation
        runner = create_memory_enabled_runner("adk_web_test")
        
        print(f"   ✅ Runner created: {type(runner)}")
        print(f"   ✅ Has memory service: {runner.memory_service is not None}")
        print(f"   ✅ Memory service type: {type(runner.memory_service).__name__}")
        print(f"   ✅ Session service type: {type(runner.session_service).__name__}")
        
        # Check agent tools
        agent = runner.agent
        if hasattr(agent, 'tools') and agent.tools:
            tool_names = [type(tool).__name__ for tool in agent.tools]
            print(f"   ✅ Agent tools: {tool_names}")
            
            if 'PreloadMemoryTool' in tool_names:
                print("   ✅ PreloadMemoryTool is configured - memories will load automatically")
            else:
                print("   ⚠️  PreloadMemoryTool not found - memories may not load")
        else:
            print("   ⚠️  No tools configured on agent")
        
        # Check root agent export
        print(f"   ✅ Root agent available: {type(root_agent)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent configuration error: {e}")
        return False

def print_adk_web_instructions():
    """Print instructions for using with ADK Web."""
    print("\n🌐 ADK Web Usage Instructions")
    print("=" * 35)
    
    print("1. Start ADK Web with your memory-enabled agent:")
    print("   adk web --agent travel_advisor.agent:root_agent")
    print()
    
    print("2. Or use specific runner:")
    print("   adk web --runner travel_advisor.agent:create_memory_enabled_runner")
    print()
    
    print("3. Expected behavior:")
    print("   - First conversation: No previous memories")
    print("   - Agent responds and memories are saved automatically")
    print("   - New session: PreloadMemoryTool loads relevant memories")
    print("   - Agent uses memories to provide personalized responses")
    print()
    
    print("4. Test memory persistence:")
    print("   a) Tell agent about travel preferences")
    print("   b) Refresh browser or start new session")
    print("   c) Ask related questions - agent should remember")

def main():
    """Main verification function."""
    print("🚀 ADK Web Memory Configuration Check")
    print("=" * 50)
    
    config_ok = verify_adk_web_memory_config()
    
    if config_ok:
        print("\n🟢 Configuration looks good for ADK Web!")
        print_adk_web_instructions()
    else:
        print("\n🔴 Configuration issues found!")
        print("Please fix the issues above before using ADK Web")
        
    print("\n📝 Remember:")
    print("- Memory saving happens automatically in ADK Web")
    print("- No manual memory.add_session_to_memory() needed")
    print("- PreloadMemoryTool handles memory loading")
    print("- Memories persist across browser sessions")

if __name__ == "__main__":
    main()