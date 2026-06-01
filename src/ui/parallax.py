import pyray as pr


class Parallax:
    """
    Implements a parallax scrolling background effect.

    Attributes:
        container: The bounding box for the parallax background.
        textures: List of tuples containing speed and texture for each layer.
        texture_origin_xs: List of current X offsets for each layer.
        dispersion: Multiplier for speed between successive layers.
        _default_textures: List of original textures used for recalculating speed.
        _last_fps: Last known frames per second setting.
    """

    def __init__(
        self,
        *,
        textures: list[pr.Texture],
        container: pr.Rectangle,
        fps: float = 50.0,
        dispersion: float = 1.05,
    ) -> None:
        """
        Initializes the parallax background.

        Args:
            textures: List of textures for each layer.
            container: The rectangle defining the viewport.
            fps: Base scrolling speed for the first layer.
            dispersion: Multiplier for speed between successive layers.
        """

        self.container: pr.Rectangle = container
        self.dispersion: float = dispersion
        self.textures: list[tuple[float, pr.Texture]] = []
        self.texture_origin_xs: list[float] = []
        for i in range(len(textures)):
            self.textures.append((fps * i, textures[i]))
            self.texture_origin_xs.append(0)
            fps = fps * self.dispersion

        self._default_textures: list[pr.Texture] = textures
        self._last_fps: float = fps

    def set_fps(self, fps: float) -> None:
        """
        Sets the scrolling speed by updating the base frames per second rate.

        Args:
            fps: New base frames per second for the scrolling speed.
        """
        if fps == self._last_fps:
            return

        self._last_fps = fps
        self.textures: list[tuple[float, pr.Texture]] = []
        for i in range(len(self._default_textures)):
            self.textures.append((fps * i, self._default_textures[i]))
            fps = fps * self.dispersion

    def on_update(self, dt: float) -> None:
        """
        Updates the scrolling offsets based on elapsed time.

        Args:
            dt: Delta time since the last update.
        """

        for i, ox in enumerate(self.texture_origin_xs):
            self.texture_origin_xs[i] += self.textures[i][0] * dt
            if self.texture_origin_xs[i] >= self.container.width:
                self.texture_origin_xs[i] = 0

    def on_render(self) -> None:
        """
        Renders the parallax layers within the container bounds.
        """

        pr.begin_scissor_mode(
            int(self.container.x),
            int(self.container.y),
            int(self.container.width),
            int(self.container.height),
        )

        for (_, texture), ox in zip(self.textures, self.texture_origin_xs):
            pr.draw_texture_pro(
                texture,
                pr.Rectangle(0, 0, texture.width, texture.height),
                self.container,
                pr.Vector2(ox, 0),
                0,
                pr.BLUE,
            )

            pr.draw_texture_pro(
                texture,
                pr.Rectangle(0, 0, texture.width, texture.height),
                pr.Rectangle(
                    self.container.x + self.container.width,
                    self.container.y,
                    self.container.width,
                    self.container.height,
                ),
                pr.Vector2(ox, 0),
                0,
                pr.BLUE,
            )

        pr.end_scissor_mode()
