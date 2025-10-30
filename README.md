# Cloudless Voice Assistant

A Raspberry Pi-based voice assistant featuring wake word detection, speech, timers, weather/traffic info (via free API), and a lightweight local LLM agent (via Langflow and Ollama).

## Features
- Wake word detection
- Text-to-speech (TTS)
- Timer and clock
- Weather and traffic (user brings free API keys)
- Local conversational LLM (Ollama via Langflow)

## File Structure
```
main.py                 # Entry point
config/                 # Config files for customization
core/                   # Main assistant loop, recognizer utilities
wakeword/               # Wake word detection logic
tts/                    # Text to speech logic
features/               # Timers, clocks, weather, traffic
agent/                  # LLM/Langflow/Ollama integration
```

## Setup
1. Make sure you have Python 3.9+ and pip.
2. Copy `config/config_example.yaml` to `config/config.yaml`. Add your API keys as needed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run with:
   ```bash
   python main.py
   ```

## Conda Environment Setup (Recommended)

To ensure everyone develops in a consistent environment, we recommend using Anaconda/Miniconda:

1. **Install Miniconda or Anaconda:**
   - Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) and install for your OS.

2. **Create an Environment:**
   ```bash
   conda create --name voice_assistant python=3.11
   ```

3. **Activate the Environment:**
   ```bash
   conda activate voice_assistant
   ```

4. **Install Python Libraries:**
   (Always activate the environment first; then run:)
   ```bash
   pip install -r requirements.txt
   ```

5. **(Optional) Check Everything Works:**
   ```bash
   python -c "import numpy, pyaudio, speech_recognition, pyttsx3, requests, yaml, pocketsphinx, gtts, langchain, openai; print('All packages installed!')"
   ```
   If no errors appear, you're set!

6. **Deactivate:**
   When you're finished:
   ```bash
   conda deactivate
   ```

> Tip: Keep your base environment clean. Always develop in your custom environment.

See module docstrings for where to add your code. Each folder/module has a clear job. For further help, see comments in code or ask the repo maintainer.