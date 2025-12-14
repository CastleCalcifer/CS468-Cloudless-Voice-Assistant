#!/bin/bash

# 1. Navigate to the correct directory
# Replace '/path/to/your/voice_assistant_directory' with the actual path
cd /path/to/your/voice_assistant_directory

# 2. Initialize Conda for the current shell session
# This line is crucial for 'conda activate' to work outside a standard terminal
# Replace '/path/to/your/conda/init' with the actual path to your Conda installation's
# initialization script (often something like /home/pi/anaconda3/etc/profile.d/conda.sh)
source /path/to/your/conda/init

# 3. Activate the Conda environment
conda activate voice_assistant_pi

# 4. Execute the Python program
python main.py 

# Optional: Keep the shell open if needed (less common for background services)
# exec bash