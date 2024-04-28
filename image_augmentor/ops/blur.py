from skimage.filters import gaussian
from skimage.exposure import rescale_intensity
import re

class Blur:
    def __init__(self, sigma):
        self.sigma = sigma

    def process(self, img):
        is_colour = len(img.shape)==3
        return rescale_intensity(gaussian(img, sigma=self.sigma, channel_axis=is_colour))
