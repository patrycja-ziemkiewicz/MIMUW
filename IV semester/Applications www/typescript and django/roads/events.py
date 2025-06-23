# roads/events.py
import time
from threading import Lock

_ping_interval = 5

_subscribers: list[list[str]] = []
_lock = Lock()

def push_event(event_str: str):
    with _lock:
        for q in _subscribers:
            q.append(event_str)

def subscribe() -> list[str]:
    q: list[str] = []
    with _lock:
        _subscribers.append(q)
    return q

def unsubscribe(q: list[str]):
    with _lock:
        _subscribers.remove(q)

def event_stream():
    
    my_queue = subscribe()
    last_ping = time.time()
    try:
        while True:
            while my_queue:
                ev = my_queue.pop(0)
                yield ev
            now = time.time()
            if now - last_ping >= _ping_interval:
                yield ': ping\n\n'
                last_ping = now

            time.sleep(1)
    finally:
        unsubscribe(my_queue)