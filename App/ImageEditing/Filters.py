from PIL import Image, ImageFilter


def sharpen_filter(image: Image.open) -> Image:
    """
    Фильтр, повышающий резкость
    """
    new_image = image.filter(ImageFilter.SHARPEN)
    return new_image


def smooth_filter(image: Image.open) -> Image:
    """
    Фильтр, понижающий резкость
    """
    new_image = image.filter(ImageFilter.SMOOTH)
    return new_image


def blur_filter(image: Image.open) -> Image:
    """
    Фильтр размытия
    """
    new_image = image.filter(ImageFilter.BLUR)
    return new_image


def find_edges_filter(image: Image.open) -> Image:
    """
    Фильтр, оставляющий только границы на изобращении
    """
    new_image = image.filter(ImageFilter.FIND_EDGES)
    return new_image


def emboss_filter(image: Image.open) -> Image:
    """
    Эффект плоского 3D
    """
    new_image = image.filter(ImageFilter.EMBOSS)
    return new_image


def black_white_filter(image: Image.open) -> Image:
    """
    Чёрно-белый фильтр
    """
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


def only_black_white_filter(image: Image.open) -> Image:
    """
    Фильтр абсолютного чб
    """
    new_image = image.copy()
    pixels = new_image.load()
    x, y = new_image.size

    if new_image.mode == 'RGBA':
        for i in range(x):
            for j in range(y):
                r, g, b, a = pixels[i, j]

                if (r + g + b) >= 400:
                    pixels[i, j] = 255, 255, 255, a
                else:
                    pixels[i, j] = 0, 0, 0, a
    else:
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]

                if (r + g + b) >= 400:
                    pixels[i, j] = 255, 255, 255
                else:
                    pixels[i, j] = 0, 0, 0

    return new_image


def inversion_filter(image: Image.open) -> Image:
    """
    Фильтр инферсии цветов
    """
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


def makeanagliph_filter(image: Image.open) -> Image:
    """
    Эффект стереопары [3D]
    """
    new_image = image.copy()
    im_pixels = new_image.load()
    x, y = new_image.size

    delta = 10

    if new_image.mode == 'RGBA':
        res = Image.new('RGBA', (x, y), (0, 0, 0, 0))
        res_pixels = res.load()
        for i in range(x):
            for j in range(y):
                if i >= delta:
                    r = im_pixels[i - delta, j][0]
                    g, b, a = im_pixels[i, j][1:]

                    res_pixels[i, j] = r, g, b, a
                else:
                    r, g, b, a = im_pixels[i, j]
                    res_pixels[i, j] = 0, g, b, a
    else:
        res = Image.new('RGB', (x, y), (0, 0, 0, 0))
        res_pixels = res.load()
        for i in range(x):
            for j in range(y):
                if i >= delta:
                    r = im_pixels[i - delta, j][0]
                    g, b = im_pixels[i, j][1:]

                    res_pixels[i, j] = r, g, b
                else:
                    r, g, b = im_pixels[i, j]
                    res_pixels[i, j] = 0, g, b

    return res
