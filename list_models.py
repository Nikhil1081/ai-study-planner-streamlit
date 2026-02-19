import requests

GEMINI_API_KEY = "AIzaSyBO3qiLuaIDE4lN5tfOe78owEw6onp5ZmU"

def list_models():
    """List available Gemini models"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            print("Available models:\n")
            for model in models:
                name = model.get('name', '')
                display_name = model.get('displayName', '')
                supported_methods = model.get('supportedGenerationMethods', [])
                
                if 'generateContent' in supported_methods:
                    print(f"✅ {name}")
                    print(f"   Display: {display_name}")
                    print(f"   Methods: {supported_methods}\n")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    list_models()
