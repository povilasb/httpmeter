import sys
import time


class Progress:
    """Displays responses progress."""

    def __init__(self) -> None:
        self._last_flushed = 0
        self._flush_interval = 0.2

    def update(self, status: str) -> None:
        sys.stdout.write(status)
        if self.we_should_flush():
            sys.stdout.flush()
            self._last_flushed = time.time()

    def done(self) -> None:
        sys.stdout.write('\n')
        sys.stdout.flush()

    def we_should_flush(self) -> bool:
        return time.time() > (self._last_flushed + self._flush_interval)
