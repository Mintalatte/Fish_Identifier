import numpy as np

class FlipH:
    def process(self, img):
        return np.fliplr(img)