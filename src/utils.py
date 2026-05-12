import time
import uuid


def unique_id() -> str:
    return str(uuid.uuid4())


class Timer:
    def __init__(self) -> None:
        self.reset()

    @property
    def elapsed_ms(self) -> float:
        return (time.time_ns() - self._start_at) // 1_000_000

    @property
    def elapsed_sec(self) -> int:
        return int(self.elapsed_ms // 1000)

    def reset(self) -> None:
        self._start_at = time.time_ns()
