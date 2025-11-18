
import time
from features.timer import set_duration_timer

def test_set_duration_timer_triggers_callback():
    triggered = []
    def callback():
        triggered.append(True)
    timer = set_duration_timer(1, callback)
    time.sleep(1.5)
    assert triggered
