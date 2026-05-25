import pyray as pr

from src.ui.core.utils import load_texture_from_path


class TextureManager:
    def __init__(self) -> None:
        self._cache: dict[str, pr.Texture] = {}

    def load(self, path: str) -> pr.Texture:
        if path not in self._cache:
            self._cache[path] = load_texture_from_path(path)
        return self._cache[path]

    def unload(self) -> None:
        for texture in self._cache.values():
            pr.unload_texture(texture)
        self._cache.clear()
