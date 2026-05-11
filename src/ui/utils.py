from typing import Callable, Union

DynamicIntCallback = Callable[[], int]
DynamicInt = Union[
    int,
    DynamicIntCallback,
    Callable[[], DynamicIntCallback],
]


def resolve(value: DynamicInt) -> int:
    if callable(value):
        data = value()
        if callable(data):
            return data()
        return data
    return value


def dynamic_min(*values: DynamicInt) -> Callable[[], DynamicInt]:
    if not values:
        return lambda: 0
    return lambda: min(values, key=lambda x: resolve(x))
