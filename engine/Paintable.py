from PodSix.Resource import *
from PodSix.Config import config

class Paintable:
	def __init__(self, editLayer=None):
		self.brushdown = False
		self.editLayer = editLayer
	
	def SetEditLayer(self, editLayer):
		self.editLayer = editLayer
		self.bitmap.surface = self.bitmap.surface.convert(8)
		print self.bitmap.surface.get_bitsize()
		print self.bitmap.surface.get_bytesize()
		self.bitmap.Palette(self.editLayer.Palette())
		self.bitmap.TransparentColor(0)
		self.bitmap.Fill(0)
	
	def MouseUp(self):
		self.brushdown = False
	
	def GetOffset(self, pos):
		rec = [int(r * gfx.width) for r in getattr(self, "rectangle", [0, 0])[:2]]
		return (pos[0] - rec[0], pos[1] - rec[1])
	
	def Paint(self, pos):
		new = self.GetOffset(pos)
		if self.brushdown and self.brushdown != new:
			self.bitmap.Line([self.brushdown, new], self.editLayer.color)
		else:
			self.bitmap.Pixel(new, self.editLayer.color)
		self.brushdown = new
	
	def Fill(self, pos):
		self.bitmap.FloodFill(self.GetOffset(pos), self.editLayer.color)

