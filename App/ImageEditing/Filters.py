from PIL import Image


# Самые простые фильтры
def black_white_filter(image: Image.open) -> Image:
    new_image = image.copy()
    pixels = new_image.load()
    x, y = new_image.size

    if new_image.mode == 'RGBA':
        for i in range(x):
            for j in range(y):
                r, g, b, a = pixels[i, j]
                bw = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
                pixels[i, j] = bw, bw, bw, a
    else:
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                bw = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
                pixels[i, j] = bw, bw, bw

    return new_image

def inversion_filter(image: Image.open) -> Image:
    new_image = image.copy()
    pixels = new_image.load()
    x, y = new_image.size

    if new_image.mode == 'RGBA':
        for i in range(x):  
            for j in range(y):
                r, g, b, a = pixels[i, j]
                pixels[i, j] = 255 - r, 255 - g, 255 - b, a
    else:
        for i in range(x):  
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = 255 - r, 255 - g, 255 - b

    return new_image
