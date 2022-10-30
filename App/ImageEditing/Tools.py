from typing import Union

from PIL import Image


def rotate_tool(image: Image, angle: Union[int, float]) -> Image:
    return image.rotate(angle, expand=True)
