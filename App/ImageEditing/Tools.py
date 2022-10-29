from typing import Union

from PIL import Image


def rotate_tool(image: Image, angle: Union[int, float]) -> Image:
    """Поворачивает заданное изображение, относительно его центра, на заданный угол

    Аргументы:
        image (Image): изображение для поворота
        angle (Union[int, float]): угол поворота, может быть отризательным

    Возвращается:
        Image: повёрнутое изображение
    """
    return image.rotate(angle, expand=True)


if __name__ == '__main__':
    pass
