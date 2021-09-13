import time
from OpenGL.raw.GL.VERSION.GL_1_0 import glClear, glClearColor
import glfw
import OpenGL.GL as gl


class Keys:
    """
    Namespace defining glfw specific keys constants
    """
    ACTION_PRESS = glfw.PRESS
    ACTION_RELEASE = glfw.RELEASE

    UP = glfw.KEY_UP
    LEFT = glfw.KEY_LEFT
    DOWN = glfw.KEY_DOWN
    RIGHT = glfw.KEY_RIGHT
    SPACE = glfw.KEY_SPACE
    ENTER = glfw.KEY_ENTER
    ESCAPE = glfw.KEY_ESCAPE
    PAGE_UP = glfw.KEY_PAGE_UP
    PAGE_DOWN = glfw.KEY_PAGE_DOWN

    A = glfw.KEY_A
    B = glfw.KEY_B
    C = glfw.KEY_C
    D = glfw.KEY_D
    E = glfw.KEY_E
    F = glfw.KEY_F
    G = glfw.KEY_G
    H = glfw.KEY_H
    I = glfw.KEY_I
    J = glfw.KEY_J
    K = glfw.KEY_K
    L = glfw.KEY_L
    M = glfw.KEY_M
    N = glfw.KEY_N
    O = glfw.KEY_O
    P = glfw.KEY_P
    Q = glfw.KEY_Q
    R = glfw.KEY_R
    S = glfw.KEY_S
    T = glfw.KEY_T
    U = glfw.KEY_U
    V = glfw.KEY_V
    W = glfw.KEY_W
    X = glfw.KEY_X
    Y = glfw.KEY_Y
    Z = glfw.KEY_Z


class Window:

    keys = Keys
    gl_version = (3, 3)

    def __init__(
        self,
        width,
        height,
        caption,
        resizable=True,
        fullscreen=False,
        vsync=True,
        aspect_ratio=16 / 9,
        samples=4,
        cursor=True,
    ):

        self.vsync = vsync
        self.width = width
        self.cursor = cursor
        self.height = height
        self.samples = samples
        self.caption = caption
        self.resizable = resizable
        self.fullscreen = fullscreen
        self.aspect_ratio = aspect_ratio

        if not glfw.init():
            raise ValueError("Failed to initialize glfw")

        # Configure the OpenGL context
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, self.gl_version[0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, self.gl_version[1])
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.RESIZABLE, self.resizable)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.SAMPLES, self.samples)

        monitor = None
        if self.fullscreen:
            # Use the primary monitors current resolution
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)
            self.width, self.height = mode.size.width, mode.size.height

            # Make sure video mode switching will not happen by
            # matching the desktops current video mode
            glfw.window_hint(glfw.RED_BITS, mode.bits.red)
            glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
            glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
            glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)

        self.window = glfw.create_window(
            self.width, self.height, self.caption, monitor, None
        )

        if not self.window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        if not self.cursor:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        glfw.make_context_current(self.window)

        if self.vsync:
            glfw.swap_interval(1)

        self.frames = 0
        glfw.set_key_callback(self.window, self.key_event_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_event_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_window_size_callback(self.window, self.window_resize_callback)

        self.setup()

    def close(self):
        """
        Suggest to glfw the window should be closed soon
        """
        glfw.set_window_should_close(self.window, True)

    @property
    def is_closing(self):
        """
        Checks if the window is scheduled for closing
        """
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        """
        Swap buffers, increment frame counter and pull events
        """
        glfw.swap_buffers(self.window)
        self.frames += 1
        glfw.poll_events()

    def destroy(self):
        """
        Gracefully terminate GLFW.
        This will also properly terminate the window and context
        """
        glfw.terminate()

    def show(self, clear_color=(.2, .3, .3, 1), clear=gl.GL_COLOR_BUFFER_BIT):
        """
        Run entering a blocking main loop
        """

        start_time = time.time()
        current_time = start_time
        prev_time = start_time
        frame_time = 0

        while not self.is_closing:
            current_time, prev_time = time.time(), current_time
            frame_time = max(current_time - prev_time, 1 / 1000)
            glClear(clear)
            glClearColor(*clear_color)

            self.on_input(self.window)
            self.on_draw(current_time - start_time, frame_time)
            self.swap_buffers()

        duration = time.time() - start_time
        self.destroy()
        print(
            "Duration: {0:.2f}s @ {1:.2f} FPS".format(duration, self.frames / duration)
        )

    def key_event_callback(self, window, key, scancode, action, mods):
        """
        Key event callback for glfw.
        Translates and forwards keyboard event to :py:func:`keyboard_event`

        Args:
            window: Window event origin
            key: The key that was pressed or released.
            scancode: The system-specific scancode of the key.
            action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
            mods: Bit field describing which modifier keys were held down.
        """
        if key == glfw.KEY_ESCAPE:
            self.close()

        if action == glfw.PRESS:
            self.on_key_pressed(key, mods)
        if action == glfw.RELEASE:
            self.on_key_released(key, mods)

    def mouse_event_callback(self, window, xpos, ypos):
        """
        Mouse event callback from glfw.
        Translates the events forwarding them to :py:func:`cursor_event`.

        Args:
            window: The window
            xpos: viewport x pos
            ypos: viewport y pos
        """
        # screen coordinates relative to the top-left corner
        self.on_mouse_event(xpos, ypos)

    def scroll_callback(self, window, dx, dy):
        self.on_mouse_scroll(dx, dy)

    def mouse_button_callback(self, window, button, action, mods):
        """
        Handle mouse button events and forward them to the example
        """
        # Offset button index by 1 to make it match the other libraries
        # button += 1
        # # Support left and right mouse button for now
        # if button not in [1, 2]:
        #     return

        xpos, ypos = glfw.get_cursor_pos(self.window)
        if action == glfw.PRESS:
            self.on_mouse_pressed(xpos, ypos, button, mods)
        else:
            self.on_mouse_released(xpos, ypos, button, mods)

    def window_resize_callback(self, window, width, height):
        """
        Window resize callback for glfw

        Args:
            window: The window
            width: New width
            height: New height
        """
        self.width, self.height = width, height
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        self.on_resize(self.buffer_width, self.buffer_height)

    def setup(self):
        pass

    def on_draw(self, time, frame_time):
        pass

    def on_input(self, window):
        pass

    def on_resize(self, width, height):
        pass

    def on_key_pressed(self, key, mods):
        pass

    def on_key_released(self, key, mods):
        pass

    def on_mouse_scroll(self, dx, dy):
        pass

    def on_mouse_event(self, xpos, ypos):
        pass

    def on_mouse_pressed(self, xpos, ypos, button, mods):
        pass

    def on_mouse_released(self, xpos, ypos, button, mods):
        pass


if __name__ == "__main__":
    win = Window(1280, 760, "Test")
    win.show()
