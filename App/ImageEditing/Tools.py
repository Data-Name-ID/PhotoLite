from typing import Union

from PIL import Image


def rotate_tool(image: Image, angle: Union[int, float]) -> Image:
    return image.rotate(angle, expand=True)


def flip_left_right_tool(image: Image) -> Image:
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def flip_top_bottom_tool(image: Image) -> Image:
    return image.transpose(Image.FLIP_TOP_BOTTOM)