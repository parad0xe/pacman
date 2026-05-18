from src.ui._v2.core.middlewares.background import BackgroundMiddleware
from src.ui._v2.core.middlewares.border import BorderMiddleware
from src.ui._v2.core.middlewares.text import TextMiddleware

BACKGROUND_RENDERER = BackgroundMiddleware()
BORDER_RENDERER = BorderMiddleware()
TEXT_RENDERER = TextMiddleware()
