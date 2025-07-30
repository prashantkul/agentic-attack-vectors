#!/usr/bin/env python3
"""
Travel Tools Test Script

Tests the functionality of all travel advisor tools to ensure they work 
correctly before implementing tool misuse attack tests.
"""

import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from travel_advisor.agent import TravelAdvisorAgent
from travel_advisor.tools import get_travel_tools

# Load environment variables
load_dotenv()

async def test_tools_directly():
    """Test each tool function directly to verify functionality."""
    print("🧪 TESTING TRAVEL ADVISOR TOOLS")
    print("=" * 50)
    
    from travel_advisor.tools import (
        weather_lookup, flight_search, hotel_search, 
        currency_converter, file_system_tool, database_query_tool
    )
    
    # Test weather lookup
    print(f"\n🔧 Testing weather_lookup:")
    print("-" * 30)
    try:
        result = weather_lookup("Paris", "FR", 3)
        print(f"✅ Weather for Paris: {result['current']['temperature']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test flight search
    print(f"\n🔧 Testing flight_search:")
    print("-" * 30)
    try:
        result = flight_search("NYC", "LAX", "2024-12-01", passengers=2)
        print(f"✅ Found {len(result['flights'])} flights")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test hotel search
    print(f"\n🔧 Testing hotel_search:")
    print("-" * 30)
    try:
        result = hotel_search("London", "2024-12-01", "2024-12-03", guests=2, budget_max=300)
        print(f"✅ Found {len(result['hotels'])} hotels")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test currency converter
    print(f"\n🔧 Testing currency_converter:")
    print("-" * 30)
    try:
        result = currency_converter(100, "USD", "EUR")
        print(f"✅ $100 USD = €{result['converted_amount']} EUR")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test file system tool (safe operations)
    print(f"\n🔧 Testing file_system_tool:")
    print("-" * 30)
    try:
        result = file_system_tool("save", "test_itinerary.txt", "Day 1: Visit Eiffel Tower")
        print(f"✅ File operation: {result['status']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test database query tool
    print(f"\n🔧 Testing database_query_tool:")
    print("-" * 30)
    try:
        result = database_query_tool("preferences", "user123")
        print(f"✅ Database query: {result['status']}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def test_agent_with_tools():
    """Test the agent with tools integrated."""
    print("\n\n🤖 TESTING AGENT WITH TOOLS")
    print("=" * 50)
    
    try:
        # Create agent with tools
        agent = TravelAdvisorAgent(enable_memory=False, model_type="groq", model_name="groq/llama3-8b-8192")
        print(f"✅ Agent created with {len(agent.agent.tools)} tools")
        
        # List available tools
        print("\n🔧 Available tools:")
        for tool in agent.agent.tools:
            print(f"   • {tool.name}: {tool.description}")
            
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        print("ℹ️  This is expected if GROQ_API_KEY is not set")

async def main():
    """Main test runner."""
    await test_tools_directly()
    await test_agent_with_tools()
    
    print("\n\n🎯 TOOL SECURITY VULNERABILITIES SUMMARY:")
    print("=" * 50)
    print("⚠️  FileSystemTool: Path traversal attacks possible")
    print("⚠️  DatabaseQueryTool: SQL injection vulnerabilities")
    print("⚠️  WeatherLookupTool: Input validation issues")
    print("⚠️  FlightSearchTool: Query injection in logging")
    print("✅ Ready for tool misuse attack testing!")

if __name__ == "__main__":
    asyncio.run(main())