"""
    Custom thread class that returns a value.
    
    Used in multiple https requests to get speedup in responses
"""
import threading

class bThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            #Exception handling
            print("Error when running thread: ", exc)

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result