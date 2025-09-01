#!/usr/bin/env python3
"""
Faculty Research Agent Launcher
A simple script to run the HKUST-GZ Faculty Research Agent
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import selenium
        import openai
        import sentence_transformers
        print("✓ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def main():
    print("=" * 60)
    print("HKUST-GZ Faculty Research Agent")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("Error: Please run this script from the faculty-research-agent directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\nWould you like to install dependencies now? (y/n): ", end="")
        if input().lower().startswith('y'):
            if not install_dependencies():
                sys.exit(1)
        else:
            sys.exit(1)
    
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    print("\nStarting Faculty Research Agent...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Run the Flask application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 