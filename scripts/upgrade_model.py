#!/usr/bin/env python3
"""
Model upgrade script for better LLM performance
Helps you test and switch between different local models
"""

import subprocess
import sys
import os
import requests
import json
from typing import Dict, List

def run_command(cmd: str) -> tuple[int, str]:
    """Run shell command and return exit code and output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, str(e)

def check_ollama_status() -> bool:
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_installed_models() -> List[str]:
    """Get list of installed Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
    except:
        pass
    return []

def test_model_performance(model_name: str) -> Dict:
    """Test model performance with standard commands"""
    print(f"\n🧪 Testing {model_name}...")
    
    test_commands = [
        "turn on the living room lights",
        "play jazz music and dim the bedroom lights", 
        "turn off all lights and pause music"
    ]
    
    results = {"model": model_name, "scores": {}}
    
    for cmd in test_commands:
        try:
            # Test with our enhanced prompt
            prompt = f"""You are Totoro, a smart home assistant. You MUST respond with valid JSON only.

Available actions: turn_on_lights, turn_off_lights, play_music, pause_music

RESPONSE FORMAT (MANDATORY):
{{
  "tasks": [array of task objects],
  "response": "friendly response text", 
  "success": true/false
}}

User: {cmd}
Assistant:"""

            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            }
            
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                llm_response = result.get("response", "").strip()
                
                # Score the response
                score = score_response(llm_response, cmd)
                results["scores"][cmd] = score
                print(f"  ✓ '{cmd}' -> Score: {score}/10")
            else:
                results["scores"][cmd] = 0
                print(f"  ✗ '{cmd}' -> Failed")
                
        except Exception as e:
            results["scores"][cmd] = 0
            print(f"  ✗ '{cmd}' -> Error: {e}")
    
    # Calculate average score
    scores = list(results["scores"].values())
    avg_score = sum(scores) / len(scores) if scores else 0
    results["average"] = avg_score
    
    print(f"📊 Average score: {avg_score:.1f}/10")
    return results

def score_response(response: str, command: str) -> int:
    """Score response quality (0-10)"""
    score = 0
    
    # Check if it's valid JSON (4 points)
    try:
        data = json.loads(response)
        score += 4
        
        # Check required fields (2 points each)
        if "tasks" in data:
            score += 2
        if "response" in data:
            score += 2
        if "success" in data:
            score += 2
            
    except json.JSONDecodeError:
        # Try to find JSON in response
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end > start:
            try:
                json.loads(response[start:end])
                score += 2  # Partial credit for embedded JSON
            except:
                pass
    
    return min(score, 10)

def recommend_models() -> List[Dict]:
    """Recommend models based on hardware and needs"""
    return [
        {
            "name": "llama3.2",
            "size": "2.0GB",
            "ram_needed": "8GB",
            "quality": "Good",
            "speed": "Fast",
            "description": "Current model - lightweight and fast"
        },
        {
            "name": "llama3.1:8b",
            "size": "4.7GB", 
            "ram_needed": "12GB",
            "quality": "Better",
            "speed": "Medium",
            "description": "Recommended upgrade - better understanding"
        },
        {
            "name": "mistral",
            "size": "4.1GB",
            "ram_needed": "8GB", 
            "quality": "Good",
            "speed": "Fast",
            "description": "Alternative - efficient and multilingual"
        },
        {
            "name": "codellama",
            "size": "3.8GB",
            "ram_needed": "8GB",
            "quality": "Good", 
            "speed": "Fast",
            "description": "Good for structured responses"
        },
        {
            "name": "llama3.1:70b",
            "size": "40GB",
            "ram_needed": "64GB",
            "quality": "Excellent",
            "speed": "Slow",
            "description": "Best quality but needs powerful hardware"
        }
    ]

def main():
    print("🎯 Totoro Model Performance Optimizer")
    print("=" * 50)
    
    # Check Ollama status
    if not check_ollama_status():
        print("❌ Ollama is not running. Please start it with: brew services start ollama")
        return
    
    print("✅ Ollama is running")
    
    # Get current models
    installed = get_installed_models()
    print(f"📦 Installed models: {', '.join(installed) if installed else 'None'}")
    
    # Show recommendations
    print("\n🎯 Model Recommendations:")
    recommendations = recommend_models()
    
    for i, model in enumerate(recommendations, 1):
        status = "✅ Installed" if model["name"] in installed else "⬇️ Available"
        print(f"{i}. {model['name']} ({model['size']}) - {status}")
        print(f"   Quality: {model['quality']}, Speed: {model['speed']}, RAM: {model['ram_needed']}")
        print(f"   {model['description']}")
    
    # Test current model if available
    if installed:
        current_model = installed[0]  # Test first installed model
        print(f"\n🧪 Testing current model: {current_model}")
        results = test_model_performance(current_model)
        
        if results["average"] < 7:
            print(f"\n⚠️ Current model score ({results['average']:.1f}/10) could be improved!")
            print("Consider upgrading to a better model.")
        else:
            print(f"\n✅ Current model performing well ({results['average']:.1f}/10)")
    
    # Interactive upgrade options
    print("\n🚀 Upgrade Options:")
    print("1. Install llama3.1:8b (recommended upgrade)")
    print("2. Install mistral (alternative model)")
    print("3. Install codellama (structured responses)")
    print("4. Test all installed models")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        install_and_test_model("llama3.1:8b")
    elif choice == "2":
        install_and_test_model("mistral")
    elif choice == "3":
        install_and_test_model("codellama")
    elif choice == "4":
        test_all_models(installed)
    elif choice == "5":
        print("Goodbye!")
    else:
        print("Invalid choice")

def install_and_test_model(model_name: str):
    """Install and test a specific model"""
    print(f"\n📥 Installing {model_name}...")
    exit_code, output = run_command(f"ollama pull {model_name}")
    
    if exit_code == 0:
        print(f"✅ {model_name} installed successfully")
        
        # Test the model
        results = test_model_performance(model_name)
        
        # Update config if model performs well
        if results["average"] >= 7:
            print(f"\n🎉 {model_name} performs well! Updating config...")
            update_config(model_name)
        else:
            print(f"\n⚠️ {model_name} score: {results['average']:.1f}/10 - may need more tuning")
            
    else:
        print(f"❌ Failed to install {model_name}: {output}")

def test_all_models(models: List[str]):
    """Test all installed models and compare"""
    if not models:
        print("No models installed to test")
        return
        
    print(f"\n🧪 Testing {len(models)} models...")
    results = []
    
    for model in models:
        result = test_model_performance(model)
        results.append(result)
    
    # Sort by average score
    results.sort(key=lambda x: x["average"], reverse=True)
    
    print("\n🏆 Model Performance Ranking:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['model']}: {result['average']:.1f}/10")
    
    # Recommend best model
    if results:
        best_model = results[0]
        if best_model["average"] >= 7:
            print(f"\n🎯 Recommended: {best_model['model']}")
            choice = input("Update config to use this model? (y/N): ")
            if choice.lower() == 'y':
                update_config(best_model["model"])

def update_config(model_name: str):
    """Update .env file with new model"""
    try:
        # Read current config
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update LOCAL_LLM_MODEL line
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('LOCAL_LLM_MODEL='):
                lines[i] = f'LOCAL_LLM_MODEL={model_name}\n'
                updated = True
                break
        
        # Write back
        if updated:
            with open('.env', 'w') as f:
                f.writelines(lines)
            print(f"✅ Updated config to use {model_name}")
            print("Restart Totoro to use the new model")
        else:
            print("⚠️ Could not find LOCAL_LLM_MODEL in config")
            
    except Exception as e:
        print(f"❌ Error updating config: {e}")

if __name__ == "__main__":
    main() 