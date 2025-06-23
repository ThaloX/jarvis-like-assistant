from src.core.speech import Speech

def test_speech_speak_runs(monkeypatch):
    speech = Speech()
    monkeypatch.setattr(speech.engine, "say", lambda x: None)
    monkeypatch.setattr(speech.engine, "runAndWait", lambda: None)
    speech.speak("test")
