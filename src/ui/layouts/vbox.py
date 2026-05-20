from typing_extensions import Unpack

from src.ui.layout import VerticalLayout
from src.ui.utils import DynamicInt
from src.ui.widget_group import WidgetGroup, WidgetGroupKwargs


class VBox(WidgetGroup):

    def __init__(
        self,
        *,
        center: bool = False,
        spacing: DynamicInt = 0,
        **kwargs: Unpack[WidgetGroupKwargs],
    ) -> None:
        kwargs["layout"] = VerticalLayout(spacing=spacing, center=center)
        super().__init__(**kwargs)
