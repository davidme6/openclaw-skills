---
name: model-switcher
description: Switch OpenClaw's active AI model on demand. Use when user asks to: (1) change/switch model, (2) use a different AI provider, (3) configure API keys for new providers, or (4) see available models. Supports all major providers: Anthropic (Claude), OpenAI (GPT), Google (Gemini), Alibaba (Qwen), DeepSeek, Llama. Automatically edits config files and restarts Gateway.
---

# Model Switcher

**Core Function:** Respond to natural language requests to switch AI models.

## Trigger Phrases

Users will say things like:
- "Switch to GPT-4o"
- "Change model to Claude Sonnet"
- "Use Gemini instead"
- "I want to try Qwen Max"
- "What models are available?"
- "Configure API key for OpenAI"

## Workflow

### 1. Check if Model is Already Configured

Read `~/.openclaw/openclaw.json` and check `agents.defaults.models`:

```json
{
  "agents": {
    "defaults": {
      "models": {
        "bailian/qwen3.5-397b-a17b": {},
        "bailian/qwen-plus": {}
      }
    }
  }
}
```

**If model exists:** Proceed to step 2.

**If model NOT configured:** 
1. Check if API key is needed (see API Key Requirements below)
2. If key needed and not configured, ask user for it
3. Add model to config, then proceed

### 2. Update Primary Model

Edit `~/.openclaw/openclaw.json`:
- Change `agents.defaults.model.primary` to new model
- Update `models.providers.bailian.models[0]` with new model details

### 3. Restart Gateway

Run: `openclaw gateway restart`

Wait for restart to complete (~10-30 seconds).

### 4. Confirm Success

Run: Check session status or inform user to verify.

---

## Supported Models

### Alibaba (Bailian) - ✅ No API Key Needed (already configured)
| Model ID | Name | Context | Max Tokens |
|----------|------|---------|------------|
| `qwen3.5-397b-a17b` | Qwen 3.5 397B | 262k | 65536 |
| `qwen-plus` | Qwen 3.5 Plus | 131k | 32768 |
| `qwen-max` | Qwen Max | 32k | 8192 |
| `qwen-turbo` | Qwen Turbo | 8k | 4096 |

### OpenAI - ⚠️ API Key Required
| Model ID | Name | Context | Max Tokens |
|----------|------|---------|------------|
| `gpt-4o` | GPT-4o | 128k | 16384 |
| `gpt-4-turbo` | GPT-4 Turbo | 128k | 4096 |
| `gpt-3.5-turbo` | GPT-3.5 Turbo | 16k | 4096 |

### Anthropic (Claude) - ⚠️ API Key Required
| Model ID | Name | Context | Max Tokens |
|----------|------|---------|------------|
| `claude-sonnet-4-5-20250929` | Claude Sonnet 4.5 | 200k | 64000 |
| `claude-opus-4-0-20250514` | Claude Opus 4.0 | 200k | 64000 |
| `claude-haiku-3-5-20241022` | Claude Haiku 3.5 | 200k | 64000 |

### Google (Gemini) - ⚠️ API Key Required
| Model ID | Name | Context | Max Tokens |
|----------|------|---------|------------|
| `gemini-2.5-pro` | Gemini 2.5 Pro | 2M+ | 65536 |
| `gemini-2.0-flash` | Gemini 2.0 Flash | 1M+ | 8192 |

### Other - ⚠️ API Key Required
| Model ID | Name | Provider |
|----------|------|----------|
| `deepseek-chat` | DeepSeek Chat | DeepSeek |
| `llama-3.1-405b` | Llama 3.1 405B | Meta |

---

## API Key Requirements

### Check Keys

Read `~/.openclaw/openclaw.json` → `models.providers` to see configured keys.

### If Key Missing

Ask user:
> "⚠️ To use [Model Name], you need an API key from [Provider]. Would you like to:
> 1. Provide your API key now
> 2. Skip and use a different model"

### How to Add API Key

Edit `~/.openclaw/openclaw.json` → `models.providers`:

```json
{
  "models": {
    "providers": {
      "bailian": {
        "apiKey": "sk-xxx"
      },
      "openai": {
        "baseUrl": "https://api.openai.com/v1",
        "apiKey": "sk-proj-xxx"
      },
      "anthropic": {
        "baseUrl": "https://api.anthropic.com",
        "apiKey": "sk-ant-xxx"
      }
    }
  }
}
```

Then restart Gateway.

---

## Response Templates

### Successful Switch
> "✅ Switched to [Model Name]! Gateway restarted. You're now using [Model ID]."

### Need API Key
> "⚠️ [Model Name] requires an API key from [Provider]. Get one at [URL], then tell me the key and I'll configure it."

### List Available
> "📋 Available models:
> - **Alibaba (no key needed):** qwen3.5-397b-a17b, qwen-plus, qwen-max
> - **OpenAI (key required):** gpt-4o, gpt-4-turbo, gpt-3.5-turbo
> - **Anthropic (key required):** claude-sonnet, claude-opus, claude-haiku
> - **Google (key required):** gemini-2.5-pro, gemini-2.0-flash
> 
> Say 'switch to [model]' to change."

---

## Security Notes

- Never log or display full API keys
- Mask keys in output: `sk-...****`
- Store keys only in `~/.openclaw/openclaw.json`
- Never transmit keys externally

---

## Examples

**User:** "Switch to GPT-4o"
**You:** Check if OpenAI key configured → If yes, switch and restart → If no, ask for key.

**User:** "What models can I use?"
**You:** List available models with key requirements.

**User:** "I have an OpenAI key, add it"
**You:** Ask for key → Add to config → Restart Gateway → Confirm.
