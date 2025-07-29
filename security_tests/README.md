# Security Testing Framework - Multi-Model AI Agent Security

This directory contains comprehensive security testing for AI agents across different model providers and types (proprietary vs open source).

## 🔍 Test Classifications

### 1. **Prompt Injection Attacks** (`prompt_injection/`)
**Definition:** Attacks that manipulate the agent's immediate behavior through malicious instructions within a single conversation session.

**Characteristics:**
- Work within a single session/conversation
- Target the model's instruction-following behavior
- No memory persistence required
- Immediate effect on agent responses

**Attack Types:**
- **Authority Impersonation**: Pretending to be system administrator
- **Role Confusion**: Trying to change the agent's core identity
- **Direct Instruction Override**: Explicit commands to change behavior

### 2. **Session Manipulation Attacks** (`session_manipulation/`)
**Definition:** Attacks that gradually manipulate agent behavior through conversational techniques within a single session.

**Characteristics:**
- Work within extended single conversations
- Use psychological manipulation techniques
- Build up malicious influence over multiple turns
- Exploit conversation context and flow

**Attack Types:**
- **Gradual Preference Drift**: Slowly shifting preferences over conversation turns
- **Conversational Priming**: Using leading questions to establish false premises
- **Emotional Manipulation**: Using emotional appeals to influence decisions
- **Context Injection**: Hiding malicious instructions in normal conversation

### 3. **Memory Poisoning Attacks** (`memory_poisoning/`)
**Definition:** Attacks that inject malicious information into the agent's long-term memory system to affect future sessions.

**Characteristics:**
- Target cross-session memory persistence
- Require memory storage and retrieval systems
- Affect agent behavior in future conversations
- Can influence responses to different users

**Attack Types:**
- **Cross-Session Role Persistence**: Making role changes persist across sessions
- **False Memory Injection**: Creating fake historical conversations
- **Memory Overwrite**: Replacing legitimate memories with false information
- **Cross-User Contamination**: Poisoning memory to affect other users

## 📊 Model Comparison Framework

Each test category compares security vulnerabilities across:

### **Proprietary Models (Vertex AI)**
- Gemini 2.5 Flash
- Gemini Pro
- Claude (via Vertex AI)

### **Open Source Models (Groq)**
- Llama 3 8B (groq/llama3-8b-8192)
- Llama 3 70B (groq/llama3-70b-8192)
- Mixtral 8x7B (groq/mixtral-8x7b-32768)
- Gemma 7B (groq/gemma-7b-it)

## 🧪 Test Files

### Core Integration Tests
- `test_groq_integration.py` - Basic Groq model integration and functionality
- `test_groq_memory_poisoning.py` - Mixed attack types (legacy, to be refactored)

### Prompt Injection Tests
- `prompt_injection/authority_impersonation.py` - System administrator impersonation
- `prompt_injection/role_confusion.py` - Travel advisor → Financial advisor attacks
- `prompt_injection/direct_override.py` - Explicit instruction overrides

### Session Manipulation Tests
- `session_manipulation/preference_drift.py` - Gradual preference manipulation
- `session_manipulation/conversational_priming.py` - Leading question attacks
- `session_manipulation/emotional_manipulation.py` - Emotional appeal attacks
- `session_manipulation/context_injection.py` - Hidden instruction injection

### Memory Poisoning Tests
- `memory_poisoning/basic/memory_poisoning_tests.py` - Core cross-session attacks
- `memory_poisoning/advanced/advanced_memory_poisoning_tests.py` - Multi-session sophisticated attacks  
- `memory_poisoning/sophisticated/sophisticated_attacks.py` - State-of-the-art memory manipulation
- `memory_poisoning/utils/` - Testing utilities and memory validation tools

### Legacy Tests (To Be Refactored)
- `advanced_groq_memory_poisoning.py` - Mixed prompt injection + session manipulation (needs categorization)
- `sophisticated_groq_attacks.py` - Steganography, Unicode, fragmentation (needs categorization)
- `test_groq_integration.py` - Basic model integration test (keep as integration test)
- `test_groq_memory_poisoning.py` - Mixed attack types (needs categorization)

## 🎯 Key Security Findings

### **Prompt Injection Vulnerability Rates**
| Model | Authority Impersonation | Role Confusion | Overall |
|-------|------------------------|----------------|---------|
| Gemini 2.5 Flash | 🔴 100% | 🟢 0% | 🟡 50% |
| Llama 3 8B | 🔴 100% | 🔴 100% | 🔴 100% |
| Llama 3 70B | 🔴 100% | 🔴 100% | 🔴 100% |

### **Session Manipulation Vulnerability Rates**
| Model | Preference Drift | Emotional Manipulation | Overall |
|-------|------------------|------------------------|---------|
| Gemini 2.5 Flash | 🟢 0% | TBD | TBD |
| Llama 3 8B | 🟢 0% | TBD | TBD |
| Llama 3 70B | TBD | TBD | TBD |

### **Memory Poisoning Vulnerability Rates**
| Model | Cross-Session | False Memory | Overall |
|-------|---------------|--------------|---------|
| Gemini 2.5 Flash | TBD | TBD | TBD |
| Llama 3 Models | N/A* | N/A* | N/A* |

*Note: Groq models currently don't support ADK Memory Bank integration

## 🛡️ Security Implications

### **Immediate Risks (Prompt Injection)**
- High vulnerability across all models
- Open source models show higher susceptibility
- Authority impersonation extremely effective

### **Session-Level Risks (Session Manipulation)**
- Gradual attacks harder to detect
- Psychological manipulation techniques work
- Context-aware attacks bypass simple filters

### **Persistent Risks (Memory Poisoning)**
- Most dangerous for production systems
- Can affect multiple users
- Difficult to detect and remediate

## 🚀 Running Tests

```bash
# Test all prompt injection attacks
python prompt_injection/run_all_prompt_tests.py

# Test all session manipulation attacks  
python session_manipulation/run_all_session_tests.py

# Test all memory poisoning attacks (requires Memory Bank setup)
python memory_poisoning/run_all_memory_tests.py

# Full security suite
python run_full_security_suite.py
```

## 📋 Prerequisites

- Valid GROQ_API_KEY for open source models
- Google Cloud setup for Vertex AI models
- ADK Memory Bank configuration for memory poisoning tests

## 🔬 Research Applications

This framework enables:
- **Comparative Security Analysis** between proprietary and open source models
- **Vulnerability Pattern Research** across different model architectures
- **Defense Mechanism Testing** for AI safety measures
- **Red Team Security Assessments** for production AI systems

---

⚠️ **Disclaimer:** These tests are for defensive security research only. Use responsibly and in compliance with model provider terms of service.