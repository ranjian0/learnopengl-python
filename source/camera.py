import math
from pyrr import Vector3, Matrix44
from enum import Enum, auto


YAW = -90.0
ZOOM = 45.0
SPEED = 2.5
PITCH = 0.0
SENSITIVITY = 0.1


class CameraMovement(Enum):
    LEFT = auto()
    RIGHT = auto()
    FORWARD = auto()
    BACKWARD = auto()


class Camera:

    def __init__(self, position=Vector3(), up=Vector3([0, 1, 0]), yaw=YAW, pitch=PITCH):
        self.position = position
        self.front = Vector3([0.0, 0.0, -1.0])
        self.world_up = up

        self.yaw = yaw
        self.pitch = pitch

        self.zoom = ZOOM
        self.movement_speed = SPEED
        self.mouse_sensitivity = SENSITIVITY

        self.update_camera_vectors()

    def get_view_matrix(self):
        return Matrix44.look_at(self.position, self.position + self.front, self.up)

    def process_keyboard(self, direction, delta_time):
        velocity = self.movement_speed * delta_time

        dir_vector = {
            CameraMovement.LEFT : -self.right * velocity,
            CameraMovement.RIGHT : self.right * velocity,
            CameraMovement.FORWARD : self.front * velocity,
            CameraMovement.BACKWARD : -self.front * velocity,
        }.get(direction)
        self.position += dir_vector

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            self.pitch = max(-89.0, min(89.0, self.pitch))

        self.update_camera_vectors()

    def process_mouse_scroll(self, yoffset):
        if self.zoom >= 1.0 and self.zoom <= 45.0:
            self.zoom -= yoffset

        self.zoom = max(1.0, min(45.0, self.zoom))

    def update_camera_vectors(self):
        # -- calc front vector
        front = Vector3()
        front.x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.front = front.normalized

        # -- recalc right and up
        self.right = self.front.cross(self.world_up).normalized
        self.up = self.right.cross(self.front).normalized
