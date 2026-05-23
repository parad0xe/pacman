import pyray as pr


class Parallax:
    def __init__(
        self,
        *,
        textures: list[pr.Texture],
        container: pr.Rectangle,
        fps: float = 50.0,
        dispersion: float = 1.05,
    ) -> None:
        self.container: pr.Rectangle = container
        self.textures: list[tuple[float, pr.Texture]] = []
        self.texture_origin_xs: list[float] = []
        for i in range(len(textures)):
            self.textures.append((fps * i, textures[i]))
            self.texture_origin_xs.append(0)
            fps = fps * dispersion

    def on_update(self, dt: float) -> None:
        for i, ox in enumerate(self.texture_origin_xs):
            self.texture_origin_xs[i] += self.textures[i][0] * dt
            if self.texture_origin_xs[i] >= self.container.width:
                self.texture_origin_xs[i] = 0

    def on_render(self) -> None:
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
