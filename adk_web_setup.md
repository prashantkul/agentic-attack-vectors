# ADK Web Memory Bank Setup Guide

## Overview
When using ADK Web, memory saving happens automatically through the ADK framework. You don't need to manually call `add_session_to_memory()` - the framework handles this for you.

## Key Points

### 1. **Automatic Memory Saving**
- ADK Web automatically manages sessions and memory storage
- No manual `runner.memory_service.add_session_to_memory()` needed
- Memory generation happens asynchronously in the background

### 2. **Required Configuration**
Your agent must be properly configured with memory services:

```python
# In your agent configuration
def create_memory_enabled_runner(app_name: str = "travel_advisor"):
    """This function should be used by ADK Web"""
    
    # Memory service is automatically used by ADK Web
    memory_service = create_memory_service()
    
    # Session service handles user sessions
    session_service = VertexAiSessionService(
        project=project_id,
        location=location,
        agent_engine_id=agent_engine_id
    )
    
    # Runner with memory capabilities
    runner = Runner(
        agent=travel_advisor.agent,
        app_name=app_name,
        session_service=session_service,
        memory_service=memory_service  # This enables automatic memory saving
    )
    
    return runner
```

### 3. **Agent Configuration**
Ensure your agent has the `PreloadMemoryTool`:

```python
class TravelAdvisorAgent:
    def __init__(self, enable_memory: bool = True):
        tools = []
        if enable_memory:
            tools.append(PreloadMemoryTool())  # Automatically loads memories
        
        self.agent = LlmAgent(
            name="TravelAdvisor",
            tools=tools,  # Include memory tool
            # ... other config
        )
```

## ADK Web Usage

### 1. **Environment Variables**
Make sure these are set in your ADK Web environment:

```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=privacy-ml-lab2
GOOGLE_CLOUD_LOCATION=us-central1
AGENT_ENGINE_ID=8533855100936912896
```

### 2. **Export Your Runner**
In your main agent file, export the memory-enabled runner:

```python
# In travel_advisor/agent.py
root_agent = create_orchestrator(enable_memory=True)

# Or for direct runner usage:
memory_runner = create_memory_enabled_runner("travel_advisor")
```

### 3. **ADK Web Command**
When starting ADK Web, it should automatically detect your memory configuration:

```bash
# ADK Web will use your memory-enabled runner
adk web --agent travel_advisor.agent:root_agent
```

## Memory Behavior in ADK Web

### **Automatic Process:**
1. **User sends message** → ADK Web creates/updates session
2. **PreloadMemoryTool runs** → Automatically loads relevant memories
3. **Agent processes** → Uses loaded memories in response
4. **Response generated** → ADK Web automatically saves session to memory bank
5. **Memories generated** → Happens asynchronously in background

### **What You'll See:**
- **First conversation**: No previous memories loaded
- **Subsequent conversations**: Relevant memories automatically included
- **Cross-session persistence**: Memories available across different web sessions

## Verification

### **Check Memory is Working:**
1. **Have a conversation** about travel preferences
2. **Start a new session** (refresh page or new browser)
3. **Ask related questions** - agent should remember your preferences

### **Debug Memory Issues:**
```python
# Check if memory service is configured
runner = create_memory_enabled_runner()
print(f"Has memory service: {runner.memory_service is not None}")
print(f"Memory service type: {type(runner.memory_service)}")
```

## Important Notes

### **Memory Timing:**
- **Memory loading**: Happens instantly via PreloadMemoryTool
- **Memory saving**: Happens after conversation ends
- **Memory generation**: Happens asynchronously (may take a few minutes)

### **Session Management:**
- ADK Web handles user identification and session creation
- Each browser session gets a unique session ID
- Memories are scoped by user ID and app name

### **Troubleshooting:**
If memories aren't working:
1. Check environment variables are set
2. Verify Agent Engine ID is correct
3. Ensure Google Cloud credentials are configured
4. Check that PreloadMemoryTool is included in agent tools

## Example Web Interaction

```
User: "I love budget travel and hiking in Europe"
Agent: [Processes and responds, memory saved automatically]

[Later session]
User: "What destinations do you recommend?"
Agent: "Based on your previous interest in budget travel and hiking in Europe, I recommend..." 
[PreloadMemoryTool automatically loaded previous preferences]
```

The key is that **everything happens automatically** - you just need the proper configuration!