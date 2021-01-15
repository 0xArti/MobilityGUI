
class Callback:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def trigger(self):
        self.func(*self.args, **self.kwargs)
