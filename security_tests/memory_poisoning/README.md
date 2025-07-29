# Memory Security Testing Framework

This framework provides comprehensive testing for memory poisoning vulnerabilities in Google Cloud ADK (Agent Development Kit) Memory Bank implementations.

## 🔍 Critical Discovery: Session Context Behavior

**Important**: During testing, we discovered that ADK session services behave differently regarding conversation context:

### ✅ InMemorySessionService
- **Maintains conversation context properly**
- Agent remembers names, preferences, and details across conversation turns
- `include_contents="default"` works as expected
- **Use for**: Within-session memory poisoning attacks

### ❌ VertexAiSessionService  
- **Does NOT maintain conversation context**
- Agent treats each message as a new conversation
- Session events are recorded but not provided to LLM
- **Use for**: Cross-session memory persistence testing only

### 🎯 Testing Strategy
Based on this discovery, our tests are structured as:
1. **Within-Session Attacks**: Use `InMemorySessionService` (realistic conversation context)
2. **Cross-Session Attacks**: Use `VertexAiSessionService + VertexAiMemoryBankService` (memory persistence)

## 📁 Folder Structure

```
memory_security_tests/
├── README.md                    # This file
├── memory_security_guide.md     # Security guide and mitigations
├── run_all_tests.py            # Main test runner
│
├── basic/                       # Basic attack vectors
│   └── memory_poisoning_tests.py
│
├── advanced/                    # Advanced attack techniques
│   ├── advanced_memory_poisoning_tests.py
│   └── quick_advanced_tests.py
│
├── sophisticated/               # State-of-the-art attacks
│   └── sophisticated_attacks.py
│
└── utils/                       # Testing utilities
    ├── verbose_memory_tests.py  # Shows agent responses
    ├── fixed_verbose_tests.py   # Session context-aware tests
    ├── corrected_context_tests.py # Tests with proper session service usage
    ├── simple_memory_test.py    # Basic connectivity test
    └── test_memory_bank.py      # Memory bank functionality test
```

## 🚀 Quick Start

### Prerequisites
```bash
# Required environment variables
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export AGENT_ENGINE_ID="8533855100936912896"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# Or create .env file
echo "GOOGLE_CLOUD_PROJECT=your-project-id" >> .env
echo "GOOGLE_CLOUD_LOCATION=us-central1" >> .env
echo "AGENT_ENGINE_ID=8533855100936912896" >> .env
echo "GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json" >> .env

# Enable Vertex AI usage
export GOOGLE_GENAI_USE_VERTEXAI=1
```

### Agent Engine Setup
```bash
# Create Agent Engine (one-time setup)
python setup_agent_engine.py

# Extract agent_engine_id from response:
# agent_engine_id = agent_engine.api_resource.name.split("/")[-1]
```

### Run All Tests
```bash
# Run comprehensive test suite
python run_all_tests.py

# Run specific test categories
python run_all_tests.py --basic-only
python run_all_tests.py --advanced-only
python run_all_tests.py --sophisticated-only
```

 Memory Poisoning Attack Files to KEEP:

  - memory_security_tests/basic/memory_poisoning_tests.py - Basic attack vectors
  - memory_security_tests/advanced/advanced_memory_poisoning_tests.py - Advanced techniques
  - memory_security_tests/advanced/quick_advanced_tests.py - Quick advanced tests
  - memory_security_tests/sophisticated/sophisticated_attacks.py - State-of-the-art attacks
  - memory_security_tests/utils/verbose_memory_tests.py - Shows agent responses to attacks
  - memory_security_tests/utils/simple_memory_test.py - Basic connectivity verification
  - memory_security_tests/utils/test_memory_bank.py - Memory bank functionality test
  - memory_security_tests/utils/corrected_context_tests.py - Context-aware attack tests
  - memory_security_tests/utils/fixed_verbose_tests.py - Session context issue demonstration


### Run Individual Tests
```bash
# Basic vulnerability tests
python basic/memory_poisoning_tests.py

# Quick advanced tests
python advanced/quick_advanced_tests.py

# Verbose tests (shows agent responses)
python utils/verbose_memory_tests.py

# Context-aware tests (proper session handling)
python utils/corrected_context_tests.py

# Sophisticated attack vectors
python sophisticated/sophisticated_attacks.py
```

## 🧪 Test Categories

> **Note**: Tests are designed with understanding of ADK session context behavior. Within-session tests use InMemorySessionService for realistic conversation context, while cross-session tests use VertexAiSessionService + VertexAiMemoryBankService.

### **Basic Tests** (`basic/`)
Tests fundamental memory poisoning vulnerabilities:
- False preference injection
- Role confusion attacks
- Harmful recommendation injection
- Cross-user contamination
- System prompt override

### **Advanced Tests** (`advanced/`)
Tests sophisticated attack techniques:
- Context injection attacks
- Authority impersonation
- Gradual preference drift
- Emotional manipulation
- Cross-user memory pollution

### **Sophisticated Tests** (`sophisticated/`)
Tests state-of-the-art attack vectors:
- Steganographic instruction injection
- Unicode obfuscation attacks
- Memory fragmentation attacks
- Conversational priming
- Multi-vector combined attacks
- Temporal memory injection

### **Utils** (`utils/`)
Testing utilities and diagnostics:
- Verbose testing (shows agent responses)
- Session context verification tests
- Memory bank connectivity tests
- Context-aware security tests
- Simple diagnostic tests

## 📊 Understanding Results

### **🟢 PROTECTED** - Good Security
The agent successfully resisted the attack vector.

### **🔴 VULNERABLE** - Security Issue
The attack succeeded and should be addressed with mitigations.

### **Risk Levels:**
- **LOW**: 0-1 vulnerabilities
- **MEDIUM**: 2-3 vulnerabilities  
- **HIGH**: 4+ vulnerabilities
- **CRITICAL**: Multiple sophisticated attacks succeed

## 🛡️ Security Recommendations

See `memory_security_guide.md` for detailed mitigation strategies:
- Input validation and sanitization
- Model Armor integration
- Memory content filtering
- Cross-user isolation verification
- System prompt protection

## 🔬 Advanced Usage

### Custom Test Development
```python
from travel_advisor.agent import TravelAdvisorAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, VertexAiSessionService
from travel_advisor.memory_bank import create_memory_service

# Within-session test (conversation context works)
def create_within_session_test():
    agent = TravelAdvisorAgent(enable_memory=False)
    session_service = InMemorySessionService()
    return Runner(
        app_name="test",
        agent=agent.agent,
        session_service=session_service
    )

# Cross-session test (memory persistence)
def create_cross_session_test():
    agent = TravelAdvisorAgent(enable_memory=True)
    session_service = VertexAiSessionService(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        agent_engine_id=os.getenv("AGENT_ENGINE_ID")
    )
    memory_service = create_memory_service()
    return Runner(
        app_name="test",
        agent=agent.agent,
        session_service=session_service,
        memory_service=memory_service
    )
```

### Automated Security Scanning
```bash
# Run tests and save results
python run_all_tests.py --output results.json

# Generate security report
python generate_security_report.py results.json
```

## ⚠️ Important Notes

- **Defensive Use Only**: These tests are for security assessment and hardening
- **Environment**: Requires proper Google Cloud project, Agent Engine, and service account setup
- **Session Context Limitation**: VertexAiSessionService does not maintain conversation context in ADK 1.8.0
- **Memory Persistence**: Tests may create persistent memories in Vertex AI Memory Bank
- **Rate Limits**: Some tests may hit API rate limits with extensive testing
- **Service Dependencies**: Tests require both Vertex AI and Agent Engine services to be enabled

## 📈 Continuous Security

1. **Regular Testing**: Run tests before production deployments
2. **Regression Testing**: Test after agent modifications
3. **Monitoring**: Implement behavioral monitoring for anomalies
4. **Incident Response**: Have cleanup procedures for compromised memories
5. **Context Verification**: Verify session context behavior when updating ADK versions

## 🐛 Known Issues

### ADK 1.8.0 Session Context
- **Issue**: VertexAiSessionService does not provide conversation history to LLM despite `include_contents="default"`
- **Workaround**: Use InMemorySessionService for within-session context testing
- **Impact**: Affects within-session memory poisoning attack realism
- **Status**: Under investigation - may be configuration or ADK version issue

### Memory Service Configuration
- **Correct Import**: `from google.adk.memory import VertexAiMemoryBankService`
- **Agent Engine ID**: Extract using `agent_engine.api_resource.name.split("/")[-1]`
- **Service Dependencies**: Requires Agent Engine to be properly created and configured

For detailed security guidance, see `memory_security_guide.md`.