#for more inspiration info check https://github.com/openai/gym/blob/master/gym/envs/classic_control/rendering.py
import pyglet
import random
from pyglet.gl import *

from schedule_sim import RESOURCES_DIR
from schedule_sim.tools.graphic_utils import colors, scale_to_window, convert_to_saturation, state_to_color


class UnrealPython():

    def __init__(self,
                 display_mode=None,
                 number_of_tasks=100,
                 square_width=50,
                 x_space_from_border=10,
                 y_space_from_border=10,
                 state_info={1: "Task 1"},
                 action_info={},
                 **kwargs):

        self._width = number_of_tasks // 10 * square_width + x_space_from_border * 2
        self._height = number_of_tasks // 10 * square_width + y_space_from_border * 2

        self._window = pyglet.window.Window(
            width=self._width, height=self._height, display=display_mode)
        glClearColor(255, 255, 255, 255)

        self._batch = pyglet.graphics.Batch()

        self._state_info, self._action_info = state_info, action_info

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # self._clear_draw()
        self._draw()

        # self._draw_background()

    #method to be called outside
    def render(self, state=[1, 1], action_idx=1, reward=-10, total_reward=-100):
        self._draw_loop(state, action_idx, reward, total_reward)
        self._draw()

    def _draw_loop(self, state, action_idx, reward, total_reward):
        self._draw_background()
        self._draw_table(state)
        self._draw_action(action_idx)
        self._draw_reward(reward, total_reward)

    def _draw(self):
        self._window.switch_to()
        self._window.dispatch_events()
        self._window.dispatch_event("on_draw")
        self._window.flip()
        self._clear_draw()

    def _clear_draw(self):
        self._window.clear()

    def _draw_background(self):
        LOGO = RESOURCES_DIR / 'logo.jpg'
        self._image_draw(LOGO, x=0, y=450, scale=0.3)

    def _draw_action(self, action_idx=1, x=400, y=470, font_size=18):
        pyglet.text.Label(
            "ACTION",
            font_name='Arial',
            bold=True,
            font_size=font_size + 3,
            color=colors['blue'],
            x=x,
            y=y + 25,
            anchor_x='center',
            anchor_y='center').draw()

        pyglet.text.Label(
            self._action_info[action_idx],
            font_name='Arial',
            bold=True,
            font_size=font_size - 3,
            color=colors['blue'],
            x=x,
            y=y,
            anchor_x='center',
            anchor_y='center').draw()

    def _draw_reward(self,
                     reward=-10,
                     total_reward=-100,
                     x=125,
                     y=370,
                     font_size=20):
        pyglet.text.Label(
            "Reward",
            font_name='Arial',
            bold=True,
            font_size=font_size + 3,
            color=colors['blue'],
            x=x,
            y=y + 25,
            anchor_x='center',
            anchor_y='center').draw()

        pyglet.text.Label(
            "{0:0.3f}".format(reward),
            font_name='Arial',
            bold=True,
            font_size=font_size - 3,
            color=colors['blue'],
            x=x,
            y=y,
            anchor_x='center',
            anchor_y='center').draw()

        pyglet.text.Label(
            "Total Reward",
            font_name='Arial',
            bold=True,
            font_size=font_size + 3,
            color=colors['blue'],
            x=x + 250,
            y=y + 25,
            anchor_x='center',
            anchor_y='center').draw()

        pyglet.text.Label(
            "{0:0.3f}".format(total_reward),
            font_name='Arial',
            bold=True,
            font_size=font_size - 3,
            color=colors['blue'],
            x=x + 250,
            y=y,
            anchor_x='center',
            anchor_y='center').draw()

    def _draw_table(self, state):
        labels = self._build_table(color_array=state)
        self._batch.draw()
        for _ in labels:
            _.draw()

    def _build_table(self,
                     color_array=[
                         1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, -.1
                     ],
                     number_of_columns=10,
                     number_of_rows=10,
                     x_space_from_border=10,
                     y_space_from_border=10,
                     square_width=50,
                     font_size=12,
                     from_the_bottom=100):

        #from bottom left (first task) to top right (last task)
        # assert len(color_array) is not 0, "State is empty!"
        # number of colors depends on the len of the array

        number_of_columns = number_of_columns
        number_of_rows = number_of_rows
        x_space_from_border = x_space_from_border
        y_space_from_border = y_space_from_border
        square_width = square_width
        line_y_min = y_space_from_border + from_the_bottom
        line_y_max = line_y_min + square_width
        labels = []
        label_counter = 0
        task_number = 0
        try:
            for __ in range(number_of_rows):
                line_x_min = x_space_from_border
                line_x_max = line_x_min + square_width
                for _ in range(number_of_columns):
                    random_color = state_to_color(color_array[task_number])
                    self._batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', [
                        line_x_min, line_y_min, line_x_min, line_y_max,
                        line_x_max, line_y_max, line_x_max, line_y_min
                    ]), ('c4B', random_color * 4))
                    labels.append(
                        pyglet.text.Label(
                            str(label_counter),
                            font_name='Arial',
                            bold=True,
                            font_size=font_size,
                            color=colors['blue'],
                            x=line_x_max - square_width // 2,
                            y=line_y_max - square_width // 2,
                            anchor_x='center',
                            anchor_y='center'))
                    label_counter += 1
                    task_number += 1
                    line_x_min = line_x_max
                    line_x_max = line_x_min + square_width
                    if task_number is len(color_array):
                        return labels
                line_y_max = line_y_min
                line_y_min = line_y_max - square_width
        except:
            print("Error when building the table, OpenGL will crash")
            import ipdb
            ipdb.set_trace()
        return labels

    def _draw_table_random_color(self,
                                 number_of_columns=10,
                                 number_of_rows=10,
                                 x_space_from_border=10,
                                 y_space_from_border=10,
                                 square_width=40,
                                 font_size=8):

        #from bottom left (first task) to top right (last task)
        # assert len(color_array) is not 0, "State is empty!"
        # number of colors depends on the len of the array

        number_of_columns = number_of_columns
        number_of_rows = number_of_rows
        x_space_from_border = x_space_from_border
        y_space_from_border = y_space_from_border
        square_width = square_width
        line_y_min = y_space_from_border
        line_y_max = line_y_min + square_width
        label_counter = 1
        labels = []
        for __ in range(number_of_rows):
            line_x_min = x_space_from_border
            line_x_max = line_x_min + square_width
            for _ in range(number_of_columns):
                random_color = colors[random.choice(list(colors.keys()))]
                self._batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', [
                    line_x_min, line_y_min, line_x_min, line_y_max, line_x_max,
                    line_y_max, line_x_max, line_y_min
                ]), ('c4B', random_color * 4))
                labels.append(
                    pyglet.text.Label(
                        str(label_counter),
                        font_name='Times New Roman',
                        font_size=8,
                        color=colors['blue'],
                        x=line_x_max - square_width // 2,
                        y=line_y_max - square_width // 2,
                        anchor_x='center',
                        anchor_y='center'))
                label_counter += 1
                line_x_min = line_x_max
                line_x_max = line_x_min + square_width
            line_y_min = line_y_max
            line_y_max = line_y_min + square_width
        self._batch.draw()
        for _ in labels:
            _.draw()

    def _image_draw(self, file_url, x=0, y=0, scale=0, title='image_stream'):
        image_stream = open(file_url, 'rb')
        image = pyglet.image.load(title, file=image_stream)
        # scale_x, scale_y = scale_to_window(image, self._window.width,
        #                                    self._window.height)
        # https://stackoverflow.com/questions/24788003/how-do-you-resize-an-image-in-python-using-pyglet
        # image.scale = min(image.height, height)/max(image.height, height)), max(min(width, image.width)/max(width, image.width)

        # import ipdb
        # ipdb.set_trace()

        sprite = pyglet.sprite.Sprite(img=image, x=x, y=y)
        sprite.update(scale=scale)
        sprite.draw()

    # method to be called outside
    def close(self):
        self._window.close()


if __name__ == "__main__":

    import ipdb
    UP = UnrealPython()

    UP.render()
    UP.render()
    ipdb.set_trace()
    UP.render()
    ipdb.set_trace()
    UP.render()
    ipdb.set_trace()
    UP.render()
    ipdb.set_trace()
    UP.close()