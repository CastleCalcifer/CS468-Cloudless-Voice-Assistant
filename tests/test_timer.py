
import time
import threading
from datetime import datetime, timedelta
from features.timer import set_duration_timer, set_time_timer


def test_set_duration_timer_triggers_callback():
    triggered = []

    def callback():
        triggered.append(True)

    timer = set_duration_timer(1, callback)
    assert isinstance(timer, threading.Timer)
    time.sleep(1.5)
    assert triggered


def test_cancel_duration_timer():
    triggered = []

    def callback():
        triggered.append(True)

    timer = set_duration_timer(1, callback)
    timer.cancel()
    time.sleep(1.3)
    assert not triggered


def test_set_time_timer_triggers_callback():
    triggered = []

    def callback():
        triggered.append(True)

    target = datetime.now() + timedelta(seconds=1)
    t = set_time_timer(target, callback)
    assert isinstance(t, threading.Timer)
    time.sleep(1.5)
    assert triggered


def test_set_time_timer_past_raises():
    past = datetime.now() - timedelta(seconds=10)
    try:
        set_time_timer(past, lambda: None)
        assert False, "Expected ValueError for past target time"
    except ValueError:
        pass
