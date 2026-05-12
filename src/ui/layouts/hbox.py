from typing import Unpack

from src.ui.layout import HorizontalLayout
from src.ui.utils import DynamicInt
from src.ui.widget_group import WidgetGroup, WidgetGroupKwargs


class HBox(WidgetGroup):
    def __init__(
        self,
        *,
        center: bool = False,
        spacing: DynamicInt = 0,
        **kwargs: Unpack[WidgetGroupKwargs],
    ) -> None:
        kwargs["layout"] = HorizontalLayout(spacing=spacing, center=center)
        super().__init__(**kwargs)
