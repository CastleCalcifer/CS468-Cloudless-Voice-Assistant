# Cloudless Voice Assistant

## Setup Instructions


### 1. Create and activate a Conda environment (Recommended)
```bash
conda create --name voice_assistant python=3.11
conda activate voice_assistant
```

### 1b. (Alternative) Create a Python venv
If you prefer a lightweight virtual environment using the standard library:

```bash
# create venv in the project root (recommended name: .venv)
python3 -m venv .venv

# activate on Linux/macOS
. .venv/bin/activate

# activate on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Notes:
- The repo includes a `.gitignore` entry for `.venv/` so the virtual environment won't be committed.
- If tests or the test runner can't import project packages, run pytest with the project root on PYTHONPATH:

```bash
PYTHONPATH=. pytest -q
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

## Neural TTS (optional)

If you want more natural, neural TTS voices locally, you can use Coqui TTS. This is optional and not required for the assistant to run.

Install in your virtualenv:

```bash
. .venv/bin/activate
pip install TTS simpleaudio
```

Quick example using the `tts` package (Coqui):

```python
from tts.neural_tts import NeuralTTS, TTS_AVAILABLE
from core.sound import play_sound

if TTS_AVAILABLE:
	tts = NeuralTTS(model_name='tts_models/en/ljspeech/tacotron2-DDC')
	wav = tts.speak_to_file('Hello — this is a more natural voice', 'out.wav')
	play_sound(wav)
else:
	print('Neural TTS not available; install the TTS package')
```

Notes:
- The first synthesis will download the model (may be 10s–100s of MB depending on model).
- CPU-only synthesis can be slow; use a GPU-enabled PyTorch build for faster synthesis.
- You can control the neural model via `config/config.yaml` (the `audio.neural_model` key).
