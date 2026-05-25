from dataclasses import dataclass, field
from typing import Literal, Optional, TypedDict

import pyray as pr


class ElementPropertiesDef(TypedDict, total=False):
    origin: pr.Vector2

    padding: float
    margin: float
    border: float
    border_radius: float
    border_color: pr.Color
    background_color: pr.Color

    font: Optional[pr.Font]
    font_size: float | str

    text_content: str
    text_align: Literal["left", "center", "right"]
    text_color: pr.Color
    letter_spacing: float

    hover_color: pr.Color

    gap: float

    justify_content: Literal["start", "center", "end"]
    align_items: Literal["start", "center", "end"]


@dataclass
class ElementProperties:
    origin: pr.Vector2 = field(default_factory=lambda: pr.Vector2(0, 0))

    padding: float = 0.0
    margin: float = 0.0
    border: float = 0.0
    border_radius: float = 0.01
    border_color: pr.Color = pr.Color(220, 220, 220, 255)
    background_color: Optional[pr.Color] = None

    font: Optional[pr.Font] = None
    font_size: float | str = 20.0

    text_content: Optional[str] = None
    text_align: Literal["left", "center", "right"] = "center"
    text_color: pr.Color = pr.Color(40, 40, 40, 255)
    letter_spacing: float = 8.0

    hover_color: pr.Color = field(default_factory=lambda: pr.Color(0, 0, 0, 0))

    gap: float = 0.0

    justify_content: Literal["start", "center", "end"] = "start"
    align_items: Literal["start", "center", "end"] = "start"


@dataclass
class ElementBoxes:
    margin_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )
    border_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )
    padding_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )
    content_box: pr.Rectangle = field(
        default_factory=lambda: pr.Rectangle(0, 0, 0, 0)
    )
