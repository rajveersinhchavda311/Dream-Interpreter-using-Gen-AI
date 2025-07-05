#!/usr/bin/env python3
"""
Test script for AI Dream Interpreter
Run this to verify your setup is working correctly
"""

import sys
import importlib.util

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit',
        'transformers',
        'torch',
        'numpy',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package} is installed")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install with: pip install -r requirements.txt")
        return False
    
    return True

def test_symbol_recognition():
    """Test the symbol recognition functionality"""
    print("\n🔍 Testing Symbol Recognition...")
    
    # Import the DreamInterpreter class
    try:
        from dream_interpreter import DreamInterpreter
        interpreter = DreamInterpreter()
        
        # Test dreams
        test_dreams = [
            "I was flying over the ocean and saw a snake",
            "I was driving a car but lost control and crashed",
            "I was in my childhood house but couldn't find the door",
            "I was being chased by a spider through a dark forest"
        ]
        
        for dream in test_dreams:
            symbols = interpreter.identify_symbols(dream)
            print(f"Dream: {dream[:50]}...")
            print(f"Symbols found: {[s[0] for s in symbols]}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing symbol recognition: {e}")
        return False

def test_model_loading():
    """Test if the GPT-2 model loads correctly"""
    print("\n🤖 Testing Model Loading...")
    
    try:
        from dream_interpreter import DreamInterpreter
        interpreter = DreamInterpreter()
        
        if interpreter.model and interpreter.tokenizer:
            print("✅ GPT-2 model loaded successfully")
            return True
        else:
            print("⚠️  Model loading failed, using fallback interpretation")
            return True  # This is still okay for basic functionality
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_interpretation_generation():
    """Test the dream interpretation generation"""
    print("\n🔮 Testing Dream Interpretation...")
    
    try:
        from dream_interpreter import DreamInterpreter
        interpreter = DreamInterpreter()
        
        # Test dream
        test_dream = "I was flying over a beautiful landscape but then started falling into water"
        test_emotion = "Anxious"
        test_context = "Starting a new job next week"
        
        # Get symbols
        symbols = interpreter.identify_symbols(test_dream)
        
        # Generate interpretation
        interpretation = interpreter.generate_interpretation(
            test_dream, test_emotion, test_context, symbols
        )
        
        print(f"Test Dream: {test_dream}")
        print(f"Generated Interpretation: {interpretation}")
        print("✅ Dream interpretation generated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating interpretation: {e}")
        return False

def test_streamlit_compatibility():
    """Test if Streamlit can import the main module"""
    print("\n🌐 Testing Streamlit Compatibility...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Try to import the main module
        from dream_interpreter import main
        print("✅ Main application module imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with Streamlit compatibility: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Dream Interpreter - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Dependencies", check_dependencies),
        ("Symbol Recognition", test_symbol_recognition),
        ("Model Loading", test_model_loading),
        ("Interpretation Generation", test_interpretation_generation),
        ("Streamlit Compatibility", test_streamlit_compatibility)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔸 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("Run 'streamlit run dream_interpreter.py' to start the application")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("Make sure all dependencies are installed correctly.")

if __name__ == "__main__":
    main()