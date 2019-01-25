#for more inspiration info check https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py
import pyglet
from pyglet.gl import *

from schedule_sim.tools.graphic_utils import colors


class UnrealPython():

    def __init__(self, width, height, display=None):

        self._window = pyglet.window.Window(
            width=width, height=height, display=display)
        # glClearColor(1, 1, 1, 1)

        self.batch = pyglet.graphics.Batch()

        # # self._window.flip()
        # vertex_list = self.batch.add(2, pyglet.gl.GL_POINTS, None,('v2i', (10, 15, 30, 35)),\
        # ('c3B', (0, 0, 255, 0, 255, 0)))

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.clear_draw()
        self.draw()

    def render(self):
        self.draw()

    def draw(self):
        self._window.switch_to()
        self._window.dispatch_events()
        self._window.dispatch_event("on_draw")
        self._window.flip()

    def clear_draw(self):
        self._window.clear()

    def draw_background(self):
        self.clear_draw()
        # vertex_list = self.batch.add(2, pyglet.gl.GL_POINTS, None,('v2i', (10, 15, 30, 35)),\
        # ('c3B', (0, 0, 255, 0, 255, 0)))
        self.batch.add(4, pyglet.gl.GL_QUADS, None,
                       ('v2i', [10, 10, 10, 50, 390, 50, 390, 10]),
                       ('c4B', colors['yellow'] * 4))

        # self.batch.add(4, pyglet.gl.GL_QUADS, None,
        #                ('v2i', [10, 10, 10, 50, 390, 50, 390, 10]),
        #                ('c4B', white * 4))

        # self.batch.add(4, pyglet.gl.GL_POLYGON, None,
        #                ('v2i', [10, 60, 10, 110, 390, 60, 390, 110]),
        #                ('c4B', white * 4))
        # self.batch.add(4, pyglet.gl.GL_QUAD_STRIP, None,
        #                ('v2i', [10, 120, 10, 170, 390, 120, 390, 170]),
        #                ('c4B', white * 4))
        self.batch.draw()

    def image_draw(self, file_url, title='image_stream'):
        image_stream = open(file_url, 'rb')
        image = pyglet.image.load(title, file=image_stream)
        sprite = pyglet.sprite.Sprite(img=image)
        sprite.draw()

    def close(self):
        self._window.close()


if __name__ == "__main__":

    UP = UnrealPython(500, 500)

    import ipdb
    ipdb.set_trace()
    UP.draw_background()
    UP.render()
    ipdb.set_trace()

    UP.close()