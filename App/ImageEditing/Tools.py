from typing import Union

from PIL import Image


def rotate_tool(image: Image.open, angle: Union[int, float]) -> Image:
    return image.rotate(angle, expand=True)


if __name__ == '__main__':
    pass
