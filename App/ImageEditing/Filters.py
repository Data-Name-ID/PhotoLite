from PIL import Image


def black_white_filter(image: Image.open) -> Image:
    """Преобразует заданное изображение в чёрно-белое

    Аргументы:
        image (Image.open): изображение преобразования

    Возвращается:
        Image: чёрно-белое изображение
    """
    return image.convert('L')
