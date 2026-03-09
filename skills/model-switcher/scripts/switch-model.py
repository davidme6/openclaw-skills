#!/usr/bin/env python3
"""
Model Switcher for OpenClaw
Interactive CLI to switch models and manage API keys.
"""

import json
import os
import sys
import getpass
from pathlib import Path

# Available models organized by provider
MODELS = {
    "Anthropic": [
        ("claude-sonnet-4-5-20250929", "Claude Sonnet 4.5 - Balanced, recommended"),
        ("claude-opus-4-0-20250514", "Claude Opus 4.0 - Most capable"),
        ("claude-haiku-3-5-20241022", "Claude Haiku 3.5 - Fast & cheap"),
    ],
    "OpenAI": [
        ("gpt-4o", "GPT-4o - Multimodal, fast"),
        ("gpt-4-turbo", "GPT-4 Turbo"),
        ("gpt-3.5-turbo", "GPT-3.5 Turbo - Cheap"),
    ],
    "Google": [
        ("gemini-2.5-pro", "Gemini 2.5 Pro"),
        ("gemini-2.0-flash", "Gemini 2.0 Flash - Fast"),
    ],
    "Alibaba": [
        ("qwen3.5-397b-a17b", "Qwen 3.5 397B - Current default"),
        ("qwen-max", "Qwen Max"),
    ],
    "Other": [
        ("deepseek-chat", "DeepSeek Chat"),
        ("llama-3.1-405b", "Llama 3.1 405B"),
    ],
}

# Provider to API key name mapping
PROVIDER_KEYS = {
    "Anthropic": "ANTHROPIC_API_KEY",
    "OpenAI": "OPENAI_API_KEY",
    "Google": "GOOGLE_API_KEY",
    "Alibaba": "DASHSCOPE_API_KEY",
    "DeepSeek": "DEEPSEEK_API_KEY",
}

def get_config_dir():
    """Get OpenClaw config directory."""
    return Path.home() / ".openclaw"

def get_models_json_path():
    """Find the models.json configuration file."""
    return get_config_dir() / "models.json"

def get_keys_json_path():
    """Find the keys.json configuration file."""
    return get_config_dir() / "keys.json"

def load_json(path):
    """Load JSON file safely."""
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    """Save JSON file safely."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving {path.name}: {e}")
        return False

def load_current_model():
    """Load current model from config."""
    path = get_models_json_path()
    config = load_json(path)
    return config.get("default_model", "not set")

def save_model(model_name):
    """Save new model to config."""
    path = get_models_json_path()
    config = load_json(path)
    config["default_model"] = model_name
    return save_json(path, config)

def load_api_keys():
    """Load API keys from config."""
    path = get_keys_json_path()
    return load_json(path)

def save_api_key(provider, key):
    """Save API key for a provider."""
    path = get_keys_json_path()
    keys = load_json(path)
    key_name = PROVIDER_KEYS.get(provider, f"{provider.upper()}_API_KEY")
    keys[key_name] = key
    return save_json(path, keys)

def mask_key(key):
    """Mask API key for display."""
    if not key or len(key) < 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"

def get_key_status(provider):
    """Check if API key is configured for provider."""
    keys = load_api_keys()
    key_name = PROVIDER_KEYS.get(provider, f"{provider.upper()}_API_KEY")
    return keys.get(key_name)

def show_main_menu():
    """Display main menu."""
    print("\n" + "="*60)
    print("🤖 OpenClaw Model & API Key Manager")
    print("="*60)
    
    current_model = load_current_model()
    print(f"\n📌 Current Model: {current_model}")
    
    print("\n🔑 API Key Status:")
    for provider, key_name in PROVIDER_KEYS.items():
        keys = load_api_keys()
        key = keys.get(key_name)
        status = f"✅ {mask_key(key)}" if key else "❌ Not configured"
        print(f"   {provider}: {status}")
    
    print("\n" + "="*60)
    print("[1] Switch Model")
    print("[2] Configure API Key")
    print("[3] Remove API Key")
    print("[4] List All Models")
    print("[5] Restart Gateway")
    print("[0] Exit")
    print("="*60)
    
    return input("\nSelect option (0-5): ").strip()

def show_model_menu():
    """Display model selection menu."""
    print("\n" + "="*60)
    print("📋 Select Model")
    print("="*60)
    
    current = load_current_model()
    idx = 1
    model_map = {}
    
    for provider, models in MODELS.items():
        print(f"\n{provider}:")
        print("-" * 40)
        for model_id, description in models:
            marker = " ⭐ CURRENT" if model_id == current else ""
            print(f"  [{idx}] {model_id}{marker}")
            print(f"      {description}")
            model_map[idx] = model_id
            idx += 1
    
    print("\n" + "="*60)
    print("[0] Back")
    print("="*60)
    
    return model_map

def show_provider_menu():
    """Display provider selection for API key config."""
    print("\n" + "="*60)
    print("🔑 Select Provider for API Key")
    print("="*60)
    
    idx = 1
    provider_map = {}
    
    for provider in PROVIDER_KEYS.keys():
        key = get_key_status(provider)
        status = "✅ Configured" if key else "❌ Not set"
        print(f"  [{idx}] {provider} - {status}")
        provider_map[idx] = provider
        idx += 1
    
    print("\n" + "="*60)
    print("[0] Back")
    print("="*60)
    
    return provider_map

def configure_api_key():
    """Configure API key for a provider."""
    provider_map = show_provider_menu()
    
    try:
        choice = input("\nSelect provider (number): ").strip()
        
        if choice == "0":
            return
        
        if choice.isdigit() and int(choice) in provider_map:
            provider = provider_map[int(choice)]
            key_name = PROVIDER_KEYS.get(provider, f"{provider.upper()}_API_KEY")
            
            print(f"\n📝 Enter API key for {provider}:")
            print(f"   (Key name: {key_name})")
            print("   (Input will be hidden)")
            
            # Try to hide input, fallback to normal input
            try:
                key = getpass.getpass("   API Key: ")
            except:
                key = input("   API Key: ")
            
            if key and len(key) > 5:
                if save_api_key(provider, key):
                    print(f"\n✅ API key for {provider} saved successfully!")
                    print("   Restart Gateway to apply changes.")
                else:
                    print("\n❌ Failed to save API key.")
            else:
                print("\n❌ Invalid key length.")
        else:
            print("\n❌ Invalid selection.")
    
    except KeyboardInterrupt:
        print("\n\nCancelled.")

def remove_api_key():
    """Remove API key for a provider."""
    provider_map = show_provider_menu()
    
    try:
        choice = input("\nSelect provider to remove key (number): ").strip()
        
        if choice == "0":
            return
        
        if choice.isdigit() and int(choice) in provider_map:
            provider = provider_map[int(choice)]
            key_name = PROVIDER_KEYS.get(provider, f"{provider.upper()}_API_KEY")
            
            keys = load_api_keys()
            if key_name in keys:
                del keys[key_name]
                if save_json(get_keys_json_path(), keys):
                    print(f"\n✅ API key for {provider} removed!")
                else:
                    print("\n❌ Failed to remove key.")
            else:
                print(f"\n⚠️  No key configured for {provider}.")
        else:
            print("\n❌ Invalid selection.")
    
    except KeyboardInterrupt:
        print("\n\nCancelled.")

def list_models():
    """List all available models."""
    print("\n" + "="*60)
    print("📋 Available Models")
    print("="*60)
    
    current = load_current_model()
    
    for provider, models in MODELS.items():
        print(f"\n{provider}:")
        for model_id, description in models:
            marker = " ⭐ CURRENT" if model_id == current else ""
            print(f"  • {model_id}{marker}")
            print(f"    {description}")

def restart_gateway():
    """Prompt to restart Gateway."""
    print("\n" + "="*60)
    print("🔄 Restart Gateway")
    print("="*60)
    print("\nChanges will take effect after Gateway restart.")
    print("\nRun this command to restart:")
    print("   openclaw gateway restart")
    print("\nOr press Enter to run it now...")
    
    input()
    
    import subprocess
    try:
        subprocess.run(["openclaw", "gateway", "restart"], check=True)
        print("\n✅ Gateway restarted!")
    except Exception as e:
        print(f"\n⚠️  Could not restart automatically: {e}")
        print("   Please run: openclaw gateway restart")

def main():
    args = sys.argv[1:]
    
    # Handle --list
    if "--list" in args:
        list_models()
        return
    
    # Handle --current
    if "--current" in args:
        current = load_current_model()
        keys = load_api_keys()
        print(f"Current model: {current}")
        print("\nConfigured API keys:")
        for provider, key_name in PROVIDER_KEYS.items():
            key = keys.get(key_name)
            if key:
                print(f"  {provider}: {mask_key(key)}")
        return
    
    # Handle --model <name>
    if "--model" in args:
        idx = args.index("--model")
        if idx + 1 < len(args):
            model_name = args[idx + 1]
            if save_model(model_name):
                print(f"✅ Switched to: {model_name}")
                print("\n⚠️  Restart Gateway for changes to take effect:")
                print("   openclaw gateway restart")
            return
        else:
            print("❌ Please specify a model name after --model")
            return
    
    # Handle --key --provider <name>
    if "--key" in args:
        configure_api_key()
        return
    
    # Interactive mode
    while True:
        choice = show_main_menu()
        
        if choice == "0":
            print("\n👋 Goodbye!")
            return
        
        elif choice == "1":
            # Switch Model
            model_map = show_model_menu()
            try:
                model_choice = input("\nSelect model (number): ").strip()
                
                if model_choice == "0":
                    continue
                
                if model_choice.isdigit() and int(model_choice) in model_map:
                    selected = model_map[int(model_choice)]
                    if save_model(selected):
                        print(f"\n✅ Switched to: {selected}")
                        print("\n⚠️  Restart Gateway for changes to take effect:")
                        print("   openclaw gateway restart")
                        
                        restart = input("\nRestart Gateway now? (y/n): ").strip().lower()
                        if restart == 'y':
                            restart_gateway()
                    else:
                        print("\n❌ Failed to save model.")
                else:
                    print("\n❌ Invalid selection.")
            except KeyboardInterrupt:
                print("\n\nCancelled.")
        
        elif choice == "2":
            # Configure API Key
            configure_api_key()
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            # Remove API Key
            remove_api_key()
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            # List Models
            list_models()
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            # Restart Gateway
            restart_gateway()
            return
        
        else:
            print("\n❌ Invalid option.")

if __name__ == "__main__":
    main()
