from skimage import transform
import re

class Rotate:
    def __init__(self, angle):
        self.angle = angle

    def process(self, img):
        return transform.rotate(img, -self.angle)
