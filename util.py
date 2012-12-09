import Image


def hist_similar(h1, h2):
    assert len(h1) == len(h2)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) \
        for l, r in zip(h1, h2)) / len(h1)


def calc_similar(i1, i2):
    return hist_similar(i1.histogram(), i2.histogram())


def calc_similar_by_path(path1, path2):
    return calc_similar(image_preprocess(path1), image_preprocess(path2))


def image_preprocess(path):
    max_width = 300
    image = Image.open(path)
    size = image.size
    if size[0] > max_width:
        image = image.resize(
            (max_width, int(1.0 * size[1] / size[0] * max_width)))
    return image


if __name__ == '__main__':
    print calc_similar_by_path(r'E:\rosi2\10\29.JPEG', 'E:\\rosi2\\10\\30.JPEG')
