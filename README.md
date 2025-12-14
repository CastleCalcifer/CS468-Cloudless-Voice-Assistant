# Cloudless Voice Assistant

## Setup Instructions

### 0. Set up the Raspberry Pi external environment

The following assumes that you have installed Raspberry Pi 5 64-bit OS and are working with aarch64 architecture.

```bash
# Get the latest Miniforge installer for AArch64 from the GitHub releases page
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh -O miniforge.sh
bash miniforge.sh
# Get sound dependencies
sudo apt install libasound2-dev
sudo apt install pulseaudio pulseaudio-utils pavucontrol
sudo apt install portaudio19-dev python3-pyaudio
sudo apt-get install flac
# Get LLM
curl -fsSL https://ollama.com/install.sh | sh
ollama run qwen2.5:1.5b-instruct
```
In order to have this program run on boot you will also need to do the following:
```bash
# change /path/to/your/project/folder/start_voice_assistant.sh
cd ~/.config/autostart
echo "[Desktop Entry]
Type=Application
Name=Voice Assistant Startup
Exec=/path/to/your/project/folder/start_voice_assistant.sh
Terminal=false
```
```bash
# change start_assistant.sh to use your project directories
# start_assistant.sh is in the main folder of the voice assistant directory
```


### 1. Create and activate a Conda environment (Recommended)
```bash
conda create --name voice_assistant_pi python=3.11
conda activate voice_assistant_pi
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
SpeechRecognition
pocketsphinx
PyYAML
requests
pyaudio
playsound==1.2.2
pytest
piper-tts
```

## Notes
- Ollama must be running for LLM features. See your config for model and host settings.