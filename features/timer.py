import threading
from datetime import datetime, timedelta

def set_duration_timer(seconds:int, callback:callable) -> threading.Timer:
    """
    Sets a timer for the specified duration in seconds.
    Calls callback when time is up.
    """
    timer = threading.Timer(seconds, callback)
    timer.start()
    return timer

def set_time_timer(target_time:int, callback:callable) -> threading.Timer:
    """
    Sets a timer to go off at a specific datetime.
    Calls callback when time is up.
    """
    now = datetime.now()
    delay = (target_time - now).total_seconds()
    if delay > 0:
        return set_duration_timer(delay, callback)
    else:
        raise ValueError("Target time is in the past.")

# Example callback function
def alarm() -> None:
    print("Time's up!")

# Example usage
if __name__ == "__main__":
    # Set a timer for 5 minutes
    set_duration_timer(5 * 60, alarm)

    # Set a timer for 5:00pm today
    target = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
    
    try:
        set_time_timer(target, alarm)
    except ValueError as e:
        print(e)
