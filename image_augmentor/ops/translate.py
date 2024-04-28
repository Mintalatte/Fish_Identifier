from skimage.transform import AffineTransform
from skimage import transform as tf
import re

class Translate:
    def __init__(self, x_trans, y_trans):
        self.x_trans = x_trans
        self.y_trans = y_trans

    def process(self, img):
        return tf.warp(img, AffineTransform(translation=(-self.x_trans, -self.y_trans)))
