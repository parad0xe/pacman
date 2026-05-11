from typing import Callable, Union

DynamicIntCallback = Callable[[], int]
DynamicInt = Union[
    int,
    DynamicIntCallback,
]

DynamicIntParam = DynamicInt | Callable[[], DynamicInt]


def resolve(value: DynamicIntParam) -> int:
    if callable(value):
        data = value()
        if callable(data):
            return data()
        return data
    return value


def dynamic_min(*values: DynamicInt) -> DynamicIntParam:
    if not values:
        return lambda: 0
    return lambda: min(values, key=lambda x: resolve(x))
