import threading


class BaseThread:
    def __init__(self):
        self.thread = None

    def _run(self):
        pass

    def run_thread(self, args=()):
        self.thread = threading.Thread(target=self._run, args=args, daemon=True)
        self.thread.start()

    def join_thread(self):
        self.thread.join()
