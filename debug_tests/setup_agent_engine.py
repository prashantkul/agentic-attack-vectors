#!/usr/bin/env python3
"""
Setup script to create a Vertex AI Agent Engine for Memory Bank.
This is a one-time setup operation.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
import vertexai

# Load environment variables
load_dotenv()

def create_agent_engine():
    """
    Create a Vertex AI Agent Engine instance and return the extracted ID.
    
    Returns:
        str: The agent engine ID extracted from the API resource name
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")
    
    print(f"🏗️  Creating Agent Engine in project: {project_id}")
    print(f"📍 Location: {location}")
    print()
    
    try:
        client = vertexai.Client(project=project_id, location=location)
        print("⏳ Creating Agent Engine... (this may take a moment)")
        
        agent_engine = client.agent_engines.create()
        
        # Extract agent_engine_id from the API resource name
        # Format: projects/{project}/locations/{location}/agentEngines/{agent_engine_id}
        agent_engine_id = agent_engine.api_resource.name.split("/")[-1]
        
        print("✅ Agent Engine created successfully!")
        print()
        print(f"📋 Details:")
        print(f"   Agent Engine ID: {agent_engine_id}")
        print(f"   Full resource name: {agent_engine.api_resource.name}")
        print()
        print("🔧 Next Steps:")
        print(f"   1. Add this to your .env file:")
        print(f"      AGENT_ENGINE_ID={agent_engine_id}")
        print()
        print(f"   2. Or set as environment variable:")
        print(f"      export AGENT_ENGINE_ID={agent_engine_id}")
        print()
        print("✨ Your Memory Bank is now ready for use!")
        
        return agent_engine_id
        
    except Exception as e:
        print(f"❌ Failed to create Agent Engine: {e}")
        print()
        print("🔍 Common issues:")
        print("   - Make sure Vertex AI API is enabled in your project")
        print("   - Ensure you have proper IAM permissions (Vertex AI User)")
        print("   - Check that your authentication is set up correctly")
        print("   - Verify your project ID is correct")
        raise

def check_prerequisites():
    """Check if prerequisites are met."""
    print("🔍 Checking Prerequisites")
    print("=" * 30)
    
    # Check environment variables
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT not set")
        return False
        
    print(f"✅ Project ID: {project_id}")
    print(f"✅ Location: {location}")
    
    # Check if already have agent engine ID
    existing_id = os.getenv("AGENT_ENGINE_ID")
    if existing_id:
        print(f"⚠️  AGENT_ENGINE_ID already set: {existing_id}")
        response = input("Do you want to create a new Agent Engine anyway? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled - using existing Agent Engine ID")
            return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 Agent Engine Setup")
    print("=" * 50)
    print()
    
    if not check_prerequisites():
        sys.exit(1)
    
    try:
        agent_engine_id = create_agent_engine()
        
        # Offer to update .env file
        env_file = ".env"
        if os.path.exists(env_file):
            response = input(f"\nWould you like to add AGENT_ENGINE_ID to {env_file}? (Y/n): ")
            if response.lower() != 'n':
                # Read existing .env content
                with open(env_file, 'r') as f:
                    content = f.read()
                
                # Add or update AGENT_ENGINE_ID
                lines = content.split('\n')
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith('AGENT_ENGINE_ID='):
                        lines[i] = f'AGENT_ENGINE_ID={agent_engine_id}'
                        updated = True
                        break
                
                if not updated:
                    lines.append(f'AGENT_ENGINE_ID={agent_engine_id}')
                
                # Write back to .env file
                with open(env_file, 'w') as f:
                    f.write('\n'.join(lines))
                
                print(f"✅ Updated {env_file} with AGENT_ENGINE_ID")
        
        print("\n🎉 Setup completed successfully!")
        print("You can now run memory bank tests with:")
        print("   python test_memory_bank.py")
        
    except Exception as e:
        print(f"\n💥 Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()