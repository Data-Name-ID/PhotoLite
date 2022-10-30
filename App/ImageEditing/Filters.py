from PIL import Image


def black_white_filter(image: Image.open) -> Image:
    return image.convert('L')
