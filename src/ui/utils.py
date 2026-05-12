from typing import Callable, Union

import pyray as pr

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


def dvw(value: int) -> DynamicInt:
    return lambda: int((value / 100) * pr.get_screen_width())


def dvh(value: int) -> DynamicInt:
    return lambda: int((value / 100) * pr.get_screen_height())


def aspect_ratio(value: int) -> DynamicIntParam:
    return dynamic_min(dvw(value), dvh(value))
