import os
import google.generativeai as genai

# Set your API key here
api_key = "AIzaSyC8UQjxTufYzbEFQxminUuR1I53P-MUspE"  # User's new key

try:
    # Configure the API
    genai.configure(api_key=api_key)
    
    print("🔍 Checking available Gemini models...")
    print("=" * 50)
    
    # List available models
    models = genai.list_models()
    
    if models:
        print("✅ Available Gemini models:")
        print("-" * 30)
        for model in models:
            print(f"📋 {model.name}")
            if hasattr(model, 'description') and model.description:
                print(f"   Description: {model.description}")
            if hasattr(model, 'generation_methods') and model.generation_methods:
                print(f"   Methods: {', '.join(model.generation_methods)}")
            print()
    else:
        print("❌ No models found!")
        
    # Test a simple model
    print("🧪 Testing model access...")
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")
        print("✅ Model access successful!")
    except Exception as e:
        print(f"❌ Model access failed: {e}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if your API key is correct")
    print("2. Make sure you're using Google AI Studio API key")
    print("3. Check if Gemini API is enabled in your region")
    print("4. Try updating: pip install --upgrade google-generativeai") 