For a Linux system, there are a number of necessary changes:

### 1. Install audiobackend dependency

Playsound uses different audiobackends for different operating systems:
    Windows:    windll
    macOS:      NSSound
    Linux:      gi

Attempting to use gi can lead to a large dependency chain.  One workaround is to use an alternative audiobackend, simpleaudio.

```bash
pip install simpleaudio
```

### 2. Install TTS dependencies

Next, the audio requires a different text-to-speech engine.  One that sounds fairly natural is Piper TTS.

```bash
pip install piper-tts
```
For this, you will need to also have a voice model.  The recommended files can be acquired as follows

wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/high/en_US-amy-high.onnx
wget https://raw.githubusercontent.com/rhasspy/piper/master/voices/en/en_US/amy/high/en_US-amy-high.onnx.json

Note: the current version of the repo has the medium version of these files already available in the tts folder




