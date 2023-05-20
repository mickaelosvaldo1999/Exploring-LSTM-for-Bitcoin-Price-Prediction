#Time constants for BTools
import time

def getTime(enum):
    """get timestamp from enum"""
    if enum == "1m":
        return 60000
    elif enum == "15m":
        return 900000
    elif enum == "30m":
        return 1800000
    elif enum == "1h":
        return 3600000
    elif enum == "1d":
        return 86400000
    else:
        print("This enum does not exist")
        return 0

def now():
    """Return current timestamp in milliseconds"""
    return time.time_ns()//1000000

def pause():
    """Pause the program for x seconds"""
    time.sleep(30)