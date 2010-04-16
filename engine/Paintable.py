from PodSix.Resource import *
from PodSix.Config import config

class Paintable:
	def __init__(self, editLayer=None):
		self.brushdown = False
		self.editLayer = editLayer
	
	def SetEditLayer(self, editLayer):
		self.editLayer = editLayer
	
	def MouseUp(self, e=None):
		self.brushdown = False
	
	def GetOffset(self, pos):
		rec = [int(r * gfx.width) for r in getattr(self, "rectangle", [0, 0])[:2]]
		return (pos[0] - rec[0], pos[1] - rec[1])
	
	def Paint(self, pos):
		self.bitmap.Line([self.GetOffset(pos), self.GetOffset(pos)], self.editLayer.color)
		
	def Line(self, start, end):
		self.bitmap.Line([self.GetOffset(start), self.GetOffset(end)], self.editLayer.color)
	
	def Fill(self, pos, isLevel):
		# if it's a fully transparent level pixel, change the BG
		if isLevel and self.bitmap.Pixel(self.GetOffset(pos))[3] == 0:
			self.bgColor = tuple(self.editLayer.color[:3])
		# otherwise floodfill this sucker
		else:
			self.bitmap.FloodFill(self.GetOffset(pos), self.editLayer.color)
			
	def GetPixel(self, pos):
		"""return the colour of the pixel at pos"""
		return self.bitmap.Pixel(pos)

