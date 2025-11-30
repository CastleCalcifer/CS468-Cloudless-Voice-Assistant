import core.sound as sound
import builtins


def test_play_sound_uses_simpleaudio(monkeypatch):
    calls = {}

    class FakePlay:
        def __init__(self):
            calls['played'] = True

        def wait_done(self):
            pass

    class FakeWaveObj:
        @staticmethod
        def from_wave_file(path):
            calls['path'] = path
            class Wrapper:
                def play(self_inner):
                    calls['play'] = True
                    return FakePlay()
            return Wrapper()

    # Inject fake simpleaudio
    monkeypatch.setattr(sound, '_simpleaudio', type('M', (), {'WaveObject': FakeWaveObj}), raising=False)
    monkeypatch.setattr(sound, 'SIMPLEAUDIO_AVAILABLE', True, raising=False)

    # Ensure other players are not called
    monkeypatch.setattr(sound, 'playsound', lambda p: (_ for _ in ()).throw(AssertionError('playsound should not be called')), raising=False)
    monkeypatch.setattr('os.system', lambda cmd: (_ for _ in ()).throw(AssertionError('os.system should not be called')))

    sound.play_sound('test.wav')

    assert calls.get('path') == 'test.wav'
    assert calls.get('play') is True


def test_play_sound_uses_playsound_when_simpleaudio_unavailable(monkeypatch):
    called = {}
    monkeypatch.setattr(sound, 'SIMPLEAUDIO_AVAILABLE', False, raising=False)

    def fake_playsound(path):
        called['playsound'] = path

    monkeypatch.setattr(sound, 'playsound', fake_playsound, raising=False)
    # Prevent os.system being called
    monkeypatch.setattr('os.system', lambda cmd: (_ for _ in ()).throw(AssertionError('os.system should not be called')))

    monkeypatch.setattr(sound, 'PLAYSOUND_AVAILABLE', True, raising=False)
    sound.play_sound('notify.wav')
    assert called.get('playsound') == 'notify.wav'


def test_play_sound_falls_back_to_paplay(monkeypatch):
    monkeypatch.setattr(sound, 'SIMPLEAUDIO_AVAILABLE', False, raising=False)
    monkeypatch.setattr(sound, 'PLAYSOUND_AVAILABLE', False, raising=False)

    # which returns True only for paplay (patch core.sound.which, it's
    # imported at module load time)
    monkeypatch.setattr(sound, 'which', lambda name: True if name == 'paplay' else False)

    recorded = {}

    def fake_system(cmd):
        recorded['cmd'] = cmd

    monkeypatch.setattr('os.system', fake_system)

    sound.play_sound('alert.wav')

    assert 'paplay' in recorded.get('cmd', '')
    assert 'alert.wav' in recorded.get('cmd', '')


def test_play_sound_no_player_prints_message(monkeypatch, capsys):
    monkeypatch.setattr(sound, 'SIMPLEAUDIO_AVAILABLE', False, raising=False)
    monkeypatch.setattr(sound, 'PLAYSOUND_AVAILABLE', False, raising=False)

    # which returns False for all players (patch core.sound.which)
    monkeypatch.setattr(sound, 'which', lambda name: False)

    def raising_system(cmd):
        raise OSError('no player')

    monkeypatch.setattr('os.system', raising_system)

    sound.play_sound('missing.wav')

    captured = capsys.readouterr()
    assert 'No audio playback method available' in captured.out or 'No audio playback method available' in captured.err
