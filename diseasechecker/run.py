#!/usr/bin/env python
"""
One-click launch script for DiseaseChecker
"""

import subprocess
import sys
import os
import webbrowser
import time

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])

def setup_data():
    """Setup data files if not present"""
    print("📊 Setting up data files...")
    
    # Create directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("model", exist_ok=True)
    os.makedirs("frontend", exist_ok=True)
    
    # Check if training data exists
    if not os.path.exists("data/disease_data.csv"):
        print("⚠️ No training data found. Creating sample data...")
        # Create sample training data
        with open("data/disease_data.csv", "w") as f:
            f.write("symptoms,disease\n")
            f.write("fever,cough,fatigue,Influenza\n")
            f.write("headache,nausea,Migraine\n")
            f.write("chest_pain,shortness_of_breath,Pneumonia\n")

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting DiseaseChecker Server...")
    
    # Change to backend directory and run app
    os.chdir("backend")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:5000")
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the app
    subprocess.run([sys.executable, "app.py"])

def main():
    print("="*60)
    print("🏥 DiseaseChecker - Full Stack Application")
    print("="*60)
    
    # Step 1: Install requirements
    install_requirements()
    
    # Step 2: Setup data
    setup_data()
    
    # Step 3: Start server
    start_server()

if __name__ == "__main__":
    main()