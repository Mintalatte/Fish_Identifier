from skimage.util import random_noise
import re

class Noise:
    def __init__(self, var):
        self.var = var

    def process(self, img):
        return random_noise(img, mode='gaussian', var=self.var)
