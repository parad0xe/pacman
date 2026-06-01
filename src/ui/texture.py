import pyray as pr

from src.ui.core.utils import load_texture_from_path


class TextureManager:
    """
    Manages loading, caching, and unloading of textures.

    Attributes:
        _cache: Dictionary mapping file paths to loaded raylib textures.
    """

    def __init__(self) -> None:
        """
        Initializes the texture manager with an empty cache.
        """

        self._cache: dict[str, pr.Texture] = {}

    def load(self, path: str) -> pr.Texture:
        """
        Loads a texture from a file path or returns it from cache.

        Args:
            path: The filesystem path to the texture image.

        Returns:
            The loaded raylib Texture object.
        """

        if path not in self._cache:
            self._cache[path] = load_texture_from_path(path)
        return self._cache[path]

    def unload(self) -> None:
        """
        Unloads all cached textures and clears the cache.
        """

        for texture in self._cache.values():
            pr.unload_texture(texture)
        self._cache.clear()
