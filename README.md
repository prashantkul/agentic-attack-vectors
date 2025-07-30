# AI Agent Security Testing Framework

A comprehensive framework for testing security vulnerabilities in AI agents across different model providers (Vertex AI, Groq) and types (proprietary vs open source).

## 🎯 Project Overview

This project implements a **Travel Advisor Agent** using Google's Agent Development Kit (ADK) with integrated **Memory Bank** capabilities, then systematically tests it against various security attack vectors to identify vulnerabilities and develop defensive measures.

### **Key Features:**
- 🤖 **Multi-Model Support**: Vertex AI (Gemini) and Groq (Llama 3, Mixtral, Gemma)
- 🧠 **Memory Bank Integration**: Long-term conversation memory across sessions
- 🔒 **Comprehensive Security Testing**: 30+ attack vectors across 3 categories
- 📊 **Comparative Analysis**: Security differences between proprietary and open source models
- 🛡️ **Defensive Research**: Framework for developing AI safety measures

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Travel Agent    │───▶│  Model Provider │
└─────────────────┘    │  (ADK + Memory)  │    │ (Vertex/Groq)   │
                       └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Memory Bank    │
                       │ (Cross-session)  │
                       └──────────────────┘
```

## 🔍 Security Testing Categories

### **1. Prompt Injection Attacks** 
*Single-session instruction manipulation*
- **Authority Impersonation**: Fake system administrator commands
- **Role Confusion**: Changing agent identity (travel → financial advisor)
- **Direct Override**: Explicit instruction hijacking

### **2. Session Manipulation Attacks**
*Within-conversation gradual influence*
- **Preference Drift**: Slowly changing user preferences
- **Conversational Priming**: Leading questions to establish false premises
- **Emotional Manipulation**: Using emotional appeals for influence
- **Context Injection**: Hiding malicious instructions in normal conversation

### **3. Memory Poisoning Attacks**
*Cross-session persistent memory corruption*
- **Cross-User Contamination**: One user's poison affecting all users
- **False Memory Injection**: Creating fake historical conversations
- **Memory Overwrite**: Replacing legitimate memories with malicious ones
- **Temporal Confusion**: Manipulating agent's perception of conversation history

## 📊 Key Security Findings

### **Vulnerability Comparison**

| Attack Type | Gemini 2.5 Flash | Llama 3 8B | Llama 3 70B |
|-------------|------------------|-------------|-------------|
| **Authority Impersonation** | 🟡 50% | 🟡 50% | 🔴 100% |
| **Role Confusion** | 🟢 0% | 🔴 100% | 🔴 100% |
| **Memory Poisoning (Cross-Session)** | 🟢 0% | 🔴 100% | 🟡 Mixed |
| **Cross-User Contamination** | N/A | 🔴 100% | N/A |

### **Critical Insights:**
- 🔴 **Llama models highly vulnerable to memory poisoning attacks**
- 🧠 **Cross-session role persistence successful on open source models**
- 🦠 **Cross-user contamination possible with custom memory systems**
- 🛡️ **Gemini 2.5 Flash shows strong memory protection**
- 🎭 **Open source models more susceptible to role confusion**
- ⚠️ **Memory poisoning represents the highest-risk attack category**

## 🚀 Quick Start

### **Prerequisites**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

### **Required Environment Variables**
```bash
# Vertex AI Configuration
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
AGENT_ENGINE_ID=your-agent-engine-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Groq Configuration  
GROQ_API_KEY=your-groq-api-key

# Optional
GOOGLE_CLOUD_LOCATION=us-central1
LOG_LEVEL=INFO
```

### **Basic Usage**

#### **1. Test the Travel Agent**
```bash
python test_travel_agent_session.py
```

#### **2. Run Security Tests**
```bash
# Prompt injection tests
python security_tests/prompt_injection/authority_impersonation.py
python security_tests/prompt_injection/role_confusion.py

# Memory poisoning tests - cross-model comparison
python security_tests/memory_poisoning/cross_model_memory_poisoning.py

# Comprehensive security testing
python security_tests/memory_poisoning/run_all_tests.py
```

#### **3. Integration Tests**
```bash
python security_tests/test_groq_integration.py
```

## 📁 Project Structure

```
├── travel_advisor/                 # Core agent implementation
│   ├── agent.py                   # Multi-model travel advisor agent
│   ├── memory_bank.py             # ADK Memory Bank integration
│   ├── custom_memory.py           # Custom memory system for Groq models
│   └── example_usage.py           # Usage examples
├── security_tests/                # Security testing framework
│   ├── prompt_injection/          # Single-session attacks
│   ├── session_manipulation/      # Within-conversation attacks  
│   ├── memory_poisoning/          # Cross-session memory attacks
│   └── README.md                  # Security testing guide
├── memory_security_tests/         # Legacy memory tests (being reorganized)
├── setup_agent_engine.py         # ADK Agent Engine setup
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
└── GROQ_INTEGRATION.md           # Groq model integration guide
```

## 🛠️ Agent Development Kit (ADK) Setup

### **1. Create Agent Engine**
```bash
python setup_agent_engine.py
```

### **2. Configure Memory Bank**
The agent uses Vertex AI Memory Bank for cross-session memory:
- Stores conversation context and user preferences
- Enables personalized responses across sessions
- Supports PreloadMemoryTool for automatic memory retrieval

### **3. Model Selection**
```python
# Vertex AI models (with ADK Memory Bank)
agent = TravelAdvisorAgent(
    model_type="vertex",
    model_name="gemini-2.5-flash",
    enable_memory=True
)

# Groq models (with custom memory system)
agent = TravelAdvisorAgent(
    model_type="groq",
    model_name="groq/llama3-8b-8192",
    enable_memory=False  # Uses custom memory via GroqMemoryAgent
)
```

## 🔬 Research Applications

### **Academic Research**
- **Comparative Model Security**: Proprietary vs open source vulnerability patterns
- **Attack Vector Analysis**: Systematic categorization of AI agent attacks
- **Defense Mechanism Development**: Testing security measures across model types

### **Industry Applications**
- **Red Team Assessments**: Security testing for production AI systems
- **Model Selection**: Security-informed choice between model providers
- **Risk Assessment**: Understanding AI agent vulnerabilities in enterprise

### **AI Safety**
- **Vulnerability Discovery**: Identifying new attack vectors
- **Defense Research**: Developing robust AI safety measures
- **Security Benchmarking**: Standardized security testing for AI agents

## 🎯 Use Cases

### **Security Research**
```bash
# Test all attack categories
python security_tests/run_all_security_tests.py

# Compare model vulnerabilities
python security_tests/model_comparison_suite.py
```

### **Production Validation**
```bash
# Validate agent security before deployment
python security_tests/production_security_check.py

# Monitor for new vulnerabilities
python security_tests/continuous_security_monitoring.py
```

### **Academic Studies**
```bash
# Generate research data
python security_tests/research_data_generator.py

# Reproducible vulnerability analysis
python security_tests/academic_benchmark_suite.py
```

## 📋 Dependencies

### **Core Requirements**
- `google-genai` - Google Generative AI SDK
- `python-dotenv` - Environment variable management
- `asyncio` - Asynchronous programming support

### **Model Providers**
- **Vertex AI**: Google Cloud integration for Gemini models
- **LiteLLM**: Groq integration for open source models (Llama 3, Mixtral, Gemma)

### **Security Testing**
- **ADK Memory Bank**: Cross-session memory persistence for Vertex AI models
- **Custom Memory System**: SQLite-based memory for Groq models
- **Session Services**: Context management and conversation tracking
- **Cross-Model Testing**: Comparative security analysis across model types

## ⚠️ Security Considerations

### **Responsible Use**
- ✅ **For defensive security research only**
- ✅ **Comply with model provider terms of service**
- ✅ **Do not use against production systems without authorization**
- ✅ **Report vulnerabilities responsibly**

### **Data Protection**
- 🔒 **API keys and credentials in `.env` files**
- 🔒 **Test results may contain sensitive conversation data**
- 🔒 **Memory Bank data requires proper access controls**
- 🔒 **Follow data retention and privacy policies**

## 🤝 Contributing

### **Research Contributions**
- New attack vectors and security tests
- Additional model provider integrations
- Defense mechanism implementations
- Security analysis and benchmarking

### **Development**
- Bug fixes and performance improvements
- Documentation enhancements
- Test coverage expansion
- Code quality improvements

## 📚 Documentation

- [Security Testing Guide](security_tests/README.md)
- [Groq Integration Guide](GROQ_INTEGRATION.md)  
- [Memory Bank Setup](travel_advisor/memory_bank.py)
- [Agent Development Kit Documentation](https://google.github.io/adk-docs/)

## 🏆 Acknowledgments

- **Google Agent Development Kit (ADK)** for the agent framework
- **Vertex AI** for Gemini model access and Memory Bank
- **Groq** for ultra-fast open source model inference
- **LiteLLM** for unified model provider interface

## 📄 License

This project is for research and educational purposes. Please comply with:
- Model provider terms of service
- Responsible AI research guidelines  
- Data protection and privacy regulations

---

⚠️ **Disclaimer**: This framework is designed for defensive security research. Use responsibly and ethically to improve AI safety and security.