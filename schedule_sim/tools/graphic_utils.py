colors = {
    'white': [255] * 4,
    'black': [0] * 4,
    'red': [255, 0, 0, 255],
    'yellow': [255, 255, 0, 255],
    'blue': [0, 0, 255, 255],
    'green': [0, 255, 0, 255]
}

RESOURCES_PATH = "../../resources/"


def state_to_color(state):
    if state < 0:
        return colors['red']
    elif 0 <= state < 0.1:
        return colors['yellow']
    elif 0.1 <= state <= 1:
        #saturated green
        return [0, 255, 0, int(convert_to_saturation(state))]
    else:
        import ipdb
        ipdb.set_trace()
        raise ("STATE IS INVALID!!!")


# Convert from 0 to 1 to 0 to 255
def convert_to_saturation(saturation_level):
    return (round(saturation_level * 255))


def scale_to_window(image, width, height):

    # https://stackoverflow.com/questions/24788003/how-do-you-resize-an-image-in-python-using-pyglet
    # image.scale = min(image.height, height)/max(image.height, height)), max(min(width, image.width)/max(width, image.width)

    scale_x = min(width, image.width) / max(width, image.width)
    scale_y = min(image.height, height) / max(image.height, height)

    return scale_x, scale_y


if __name__ == '__main__':
    print("hello")