#for more inspiration info check https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py
import pyglet
from pyglet.gl import *

import random
from schedule_sim.tools.graphic_utils import colors, RESOURCES_PATH, scale_to_window, convert_to_saturation


class UnrealPython():

    def __init__(self, width=500, height=500, display=None):

        self._window = pyglet.window.Window(
            width=width, height=height, display=display)
        # glClearColor(1, 1, 1, 1)

        self._batch = pyglet.graphics.Batch()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self._clear_draw()
        self._draw()

    #method to be called outside
    def render(self):
        self._draw()

    def _draw(self):
        self._window.switch_to()
        self._window.dispatch_events()
        self._window.dispatch_event("on_draw")
        self._window.flip()

    def _clear_draw(self):
        self._window.clear()

    def _draw_background(self):
        LOGO = RESOURCES_PATH + 'logo.jpg'
        self._image_draw(LOGO)

    def _draw_table(self,
                    number_of_columns=10,
                    number_of_rows=10,
                    x_space_from_border=10,
                    y_space_from_border=10,
                    square_width=40):
        self._clear_draw()

        #from bottom left (first task) to top right (last task)

        number_of_columns = number_of_columns
        number_of_rows = number_of_rows
        x_space_from_border = x_space_from_border
        y_space_from_border = y_space_from_border
        square_width = square_width
        line_y_min = y_space_from_border
        line_y_max = line_y_min + square_width
        for __ in range(number_of_rows):
            line_x_min = x_space_from_border
            line_x_max = line_x_min + square_width
            for _ in range(number_of_columns):
                random_color = colors[random.choice(list(colors.keys()))]
                self._batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', [
                    line_x_min, line_y_min, line_x_min, line_y_max, line_x_max,
                    line_y_max, line_x_max, line_y_min
                ]), ('c4B', random_color * 4))
                line_x_min = line_x_max
                line_x_max = line_x_min + square_width
            line_y_min = line_y_max
            line_y_max = line_y_min + square_width
        # self.batch.add(4, pyglet.gl.GL_POLYGON, None,
        #                ('v2i', [10, 60, 10, 110, 390, 60, 390, 110]),
        #                ('c4B', white * 4))
        # self.batch.add(4, pyglet.gl.GL_QUAD_STRIP, None,
        #                ('v2i', [10, 120, 10, 170, 390, 120, 390, 170]),
        #                ('c4B', white * 4))
        self._batch.draw()

    def _image_draw(self, file_url, title='image_stream'):
        image_stream = open(file_url, 'rb')
        image = pyglet.image.load(title, file=image_stream)
        scale_x, scale_y = scale_to_window(image, self._window.width,
                                           self._window.height)
        # https://stackoverflow.com/questions/24788003/how-do-you-resize-an-image-in-python-using-pyglet
        # image.scale = min(image.height, height)/max(image.height, height)), max(min(width, image.width)/max(width, image.width)

        # import ipdb
        # ipdb.set_trace()

        sprite = pyglet.sprite.Sprite(img=image)
        sprite.update(scale_x=scale_x, scale_y=scale_y)
        sprite.draw()

    # method to be called outside
    def close(self):
        self._window.close()


if __name__ == "__main__":

    import ipdb
    UP = UnrealPython(500, 500)

    UP._draw_background()
    # UP._draw_table()
    UP.render()
    ipdb.set_trace()

    UP.close()