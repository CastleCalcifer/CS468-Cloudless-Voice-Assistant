from datetime import datetime

def get_time() -> str:
    """
    Returns the current time as a string.
    """
    now = datetime.now()
    hour_minute = now.strftime("%I:%M %p").lstrip('0')
    return f"It's {hour_minute}"

def get_date() -> str:
    """
    Returns the current date as a string.
    """
    now = datetime.now()
    day_of_week = now.strftime("%A")
    month = now.strftime("%B")
    day = now.day
    year = now.year
    # Add ordinal suffix to day
    def ordinal(n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix
    day_str = ordinal(day)
    return f"Today is {day_of_week}, {month} {day_str}, {year}"

if __name__ == "__main__":
    print("Current time is:", get_time())
    print("Current date is:", get_date())