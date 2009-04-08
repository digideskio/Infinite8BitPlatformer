from PodSix.Platformer.Camera import Camera
from PodSix.ArrayOps import Multiply, Subtract
from PodSix.Resource import *
from PodSix.Config import config
from PodSix.Rectangle import Rectangle

class BitCamera(Camera):
	def TranslateRectangle(self, rectangle):
		return Rectangle(Multiply(Subtract(rectangle, self.rectangle[:2] + [0, 0]), gfx.width * config.zoom))
