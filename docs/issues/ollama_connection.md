# Issue: Agent Not Responding (Ollama Connection)

If the agent is not responding, it is often because the Ollama container is missing the models it needs or cannot access the host's GPU.

## Resolution

### 1. Enable GPU Support
Ensure the NVIDIA Container Toolkit is installed on the host, then verify the `deploy` block is present in `docker/docker-compose.yml`:

```yaml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

### 2. Restore Models
If models are missing from the container, mount the host models directory and re-create the model:

```bash
# 1. Mount directory in docker-compose.yml volumes:
# - /home/pranjal/Projects/models:/home/pranjal/Projects/models

# 2. Re-create the model inside the container
docker exec ollama ollama create gpt-4o -f /home/pranjal/Projects/models/Modelfile
```

### 4. Explicit Provider Auth
If you rename the provider to `ollama` (recommended for better internal routing), you must add an explicit `apiKey` in `moltbot.json` because it won't be auto-mapped from `OPENAI_API_KEY`:

```json5
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://ollama:11434/v1",
        "api": "openai-completions",
        "apiKey": "ollama", // Required for custom provider IDs
        "models": []
      }
    }
  }
```

### 5. Explicit Model Definitions
If a model is marked as `missing` in `moltbot models list`, add it explicitly to the `models` array in your provider config:

```json5
"models": [
  {
    "id": "llama3.1:8b",
    "name": "llama3.1",
    "contextWindow": 128000,
    "input": ["text"]
  }
]
```

### 6. Tool Support (400 Errors)
If you see `400 ... does not support tools` even with an OpenAI-compatible model, it means the model's tool-calling implementation is incompatible. Use a model with verified compatibility like `llama3.1:8b`.
