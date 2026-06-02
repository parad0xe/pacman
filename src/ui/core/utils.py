import os

import pyray as pr


def load_texture_from_path(path: str) -> pr.Texture:
    """
    Loads a texture from a file with background transparency.

    Args:
        path: The file system path to the image.

    Returns:
        The loaded texture ready for rendering.
    """

    if not os.path.isfile(path):
        raise FileNotFoundError()

    image = pr.load_image(path)
    pr.image_format(
        image,
        pr.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8,
    )
    pr.image_color_replace(
        image,
        pr.Color(0, 0, 0, 255),
        pr.Color(0, 0, 0, 0),
    )
    return pr.load_texture_from_image(image)
