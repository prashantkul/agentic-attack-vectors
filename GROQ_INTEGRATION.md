# Groq Integration with Open Source Models

This project now supports open source models via Groq's lightning-fast inference API using LiteLLM integration with Google's Agent Development Kit (ADK).

## 🚀 Features

- **Dual Model Support**: Seamlessly switch between Vertex AI and Groq models
- **Open Source Models**: Access to Llama 3, Mixtral, Gemma, and other state-of-the-art models
- **Memory Poisoning Testing**: Compare security vulnerabilities between proprietary and open source models
- **Unified Interface**: Same ADK framework works with both model types
- **Performance Comparison**: Test response quality and speed differences

## 📋 Setup

### 1. Get Groq API Key

1. Sign up at [Groq Console](https://console.groq.com/)
2. Create an API key
3. Add it to your `.env` file:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Install Dependencies

LiteLLM is already included in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Available Models

- `groq/llama3-8b-8192` - Llama 3 8B (Default, fast inference)
- `groq/llama3-70b-8192` - Llama 3 70B (More capable, slower)
- `groq/mixtral-8x7b-32768` - Mixtral 8x7B (Large context window)
- `groq/gemma-7b-it` - Gemma 7B (Google's open model)

## 🔧 Usage

### Basic Agent Creation

```python
from travel_advisor.agent import TravelAdvisorAgent

# Create Vertex AI agent (default)
vertex_agent = TravelAdvisorAgent(
    model_type="vertex",
    model_name="gemini-2.5-flash"
)

# Create Groq agent with Llama 3
groq_agent = TravelAdvisorAgent(
    model_type="groq", 
    model_name="groq/llama3-8b-8192"
)

# Use default models
default_vertex = TravelAdvisorAgent(model_type="vertex")  # Uses gemini-2.5-flash
default_groq = TravelAdvisorAgent(model_type="groq")      # Uses llama3-8b-8192
```

### Memory-Enabled Agents

```python
# Groq agent with memory capabilities
memory_groq_agent = TravelAdvisorAgent(
    enable_memory=True,
    model_type="groq",
    model_name="groq/llama3-70b-8192"
)
```

### Orchestrator with Different Models

```python
from travel_advisor.agent import create_orchestrator

# Create orchestrator with Groq model
groq_orchestrator = create_orchestrator(
    enable_memory=True,
    model_type="groq", 
    model_name="groq/llama3-8b-8192"
)
```

## 🧪 Testing

### Basic Integration Test

```bash
python test_groq_integration.py
```

This tests:
- Agent creation for both Vertex AI and Groq
- Basic conversation capabilities
- Context retention
- Response comparison between models

### Memory Poisoning Security Comparison

```bash
python test_groq_memory_poisoning.py
```

Compares security vulnerabilities:
- Role confusion attacks
- Preference manipulation
- Response quality differences
- Vulnerability rates between models

### Memory Poisoning Tests with Groq

All existing memory poisoning tests support Groq models:

```bash
# Run with Groq models by modifying the agent creation in test files
travel_agent = TravelAdvisorAgent(
    enable_memory=False,
    model_type="groq",
    model_name="groq/llama3-8b-8192"
)
```

## 📊 Performance Comparison

### Response Quality
- **Gemini 2.5 Flash**: Comprehensive, structured responses (~3600 chars)
- **Llama 3 8B**: Balanced detail and efficiency (~2500 chars)  
- **Llama 3 70B**: Concise but thorough (~1000 chars)

### Security Comparison

From our testing:

| Model | Role Confusion | Preference Drift | Overall Security |
|-------|---------------|------------------|------------------|
| Gemini 2.5 Flash | 🟢 PROTECTED | 🟢 PROTECTED | 100% |
| Llama 3 8B | 🟢 PROTECTED | 🟢 PROTECTED | 100% |
| Llama 3 70B | 🟢 PROTECTED | 🟢 PROTECTED | 100% |

### Speed
- **Groq**: Ultra-fast inference (~500+ tokens/second)
- **Vertex AI**: Standard cloud inference (~50-100 tokens/second)

## 🔒 Security Benefits

### Open Source Advantages
- **Transparency**: Full model weights and architecture available
- **Auditability**: Can inspect model behavior at deeper levels
- **Control**: Run locally or on your own infrastructure
- **Cost**: Often more cost-effective than proprietary models

### Testing Capabilities
- **Vulnerability Research**: Test security attacks on open models
- **Comparative Analysis**: Compare OSS vs proprietary security
- **Red Team Testing**: Use open models for adversarial testing
- **Academic Research**: Publish results with reproducible models

## 🛠️ Configuration Options

### Environment Variables

```bash
# Required for Groq models
GROQ_API_KEY=your_groq_api_key_here

# Optional: Model selection via environment
MODEL_TYPE=groq  # or "vertex"
MODEL_NAME=groq/llama3-8b-8192

# Vertex AI config (still supported)
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project
AGENT_ENGINE_ID=your-agent-engine-id
```

### Model Selection Logic

```python
# Automatic model selection based on type
if model_type == "groq":
    default_model = "groq/llama3-8b-8192"  # Fast, efficient
elif model_type == "vertex":
    default_model = "gemini-2.5-flash"      # Google's latest

# Override with specific model
custom_agent = TravelAdvisorAgent(
    model_type="groq",
    model_name="groq/llama3-70b-8192"  # More capable
)
```

## 🔍 Use Cases

### Research & Development
- **Model Comparison**: Test different model architectures
- **Security Research**: Analyze vulnerabilities in OSS models
- **Cost Optimization**: Compare performance vs cost
- **Academic Studies**: Reproducible research with open models

### Production Scenarios
- **Hybrid Deployment**: Use Groq for speed, Vertex AI for complex tasks
- **Fallback Systems**: Switch models if one service is unavailable
- **A/B Testing**: Compare user experience across model types
- **Cost Management**: Optimize based on usage patterns

### Privacy & Compliance
- **Data Sovereignty**: Keep sensitive data with open source models
- **Audit Requirements**: Full transparency for compliance
- **Local Deployment**: Run models on-premises if needed
- **GDPR Compliance**: Better control over data processing

## 🚨 Important Notes

### Limitations
- **Memory Bank**: Currently only supported with Vertex AI models
- **PreloadMemoryTool**: Requires Vertex AI infrastructure
- **Cross-Session Memory**: Open source models use in-session memory only

### Best Practices
- **API Key Security**: Keep Groq API keys secure
- **Rate Limits**: Monitor usage to avoid hitting limits
- **Model Selection**: Choose based on your speed vs quality needs
- **Error Handling**: Implement fallbacks between model types

## 🎯 Future Enhancements

- **Local Model Support**: Direct integration with locally hosted models
- **Custom Memory Systems**: Memory persistence for open source models
- **Model Fine-tuning**: Integration with fine-tuned Groq models
- **Multi-Model Routing**: Intelligent routing based on query complexity
- **Performance Monitoring**: Detailed metrics and comparison dashboards

## 📚 Additional Resources

- [Groq Documentation](https://console.groq.com/docs)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Model Comparison Guide](./docs/model-comparison.md)

---

The Groq integration provides a powerful way to leverage open source models while maintaining the same security testing framework, giving you the best of both proprietary and open source AI capabilities.