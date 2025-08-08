#!/usr/bin/env python3
"""
Launcher script for the PBL Assistant Streamlit app
This script ensures all imports work correctly by setting up the Python path
"""
import os
import sys
import subprocess

# Add the current directory to the Python path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Run the Streamlit app
if __name__ == "__main__":
    print("Starting PBL Assistant Streamlit app...")
    subprocess.run(["streamlit", "run", os.path.join(current_dir, "streamlit_app.py")])
