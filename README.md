# Cloudless Voice Assistant

## Setup Instructions


### 1. Create and activate a Conda environment (Recommended)
```bash
conda create --name voice_assistant python=3.11
conda activate voice_assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your settings
Copy `config/config_example.yaml` to `config/config.yaml` and fill in your API keys and preferences.

### 4. Run the assistant
```bash
python main.py
```

## Requirements

All required Python packages are listed in `requirements.txt`:

```
pyttsx3
SpeechRecognition
pocketsphinx
PyYAML
requests
pyaudio
```

## Notes
- For microphone support, you may need to install `pyaudio` separately depending on your OS.
- Ollama must be running for LLM features. See your config for model and host settings.
