from PodSix.Resource import *
from PodSix.Concurrent import Concurrent
from PodSix.Rectangle import Rectangle
from PodSix.Config import config
from PodSix.GUI.Button import TextButton

class EditBox(Rectangle, Concurrent):
	def __init__(self, inlist, camera):
		inlist = camera.FromScreenCoordinates(inlist) + [0, 0]
		Rectangle.__init__(self, inlist)
		Concurrent.__init__(self)
		self.camera = camera
		self.color = (150, 150, 150)	
	
	def Draw(self):
		gfx.DrawRect(self.camera.TranslateRectangle(self), self.color, 1)
	
	def SetCorner(self, pos):
		pos = self.camera.FromScreenCoordinates(pos)
		self.Width((pos[0] - self.Left()))
		self.Height((pos[1] - self.Top()))

def editOn(fn):
	def newfn(self, *args, **kwargs):
		if self.mode and self.level:
			return fn(self, *args, **kwargs)
	return newfn

class FamilyButton(TextButton):
	family = []
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent
		TextButton.__init__(self, name, pos = {"right": 0.99, "top": 0.1 + 0.05 * len(self.family)}, colors=[[100, 100, 100], [15, 15, 15]])
		self.family.append(self)
	
	def Select(self, on=True):
		self.parent.selected = self.name
		self.colors[0] = [100 + 150 * on, 100 + 150 * on, 100 + 150 * on]
	
	def Pressed(self):
		[f.Select(False) for f in self.family]
		self.Select()
		#getattr(self.parent, 'Pressed_' + self.name)()

class EditButton(TextButton):
	def __init__(self, parent):
		self.parent = parent
		TextButton.__init__(self, "edit", pos = {"right": 0.99, "top": 0.01}, colors=[[100, 100, 100], [15, 15, 15]])
	
	def Pressed(self):
		self.parent.ToggleMode()

class EditLayer(Concurrent, EventMonitor):
	"""
	This layer holds the GUI for editing levels.
	The edit button always shows, but toggling it shows or hides the other stuff.
	"""
	def __init__(self):
		# whether edit mode is showing or not
		self.mode = False
		self.level = None
		self.editButton = EditButton(self)
		Concurrent.__init__(self)
		EventMonitor.__init__(self)
		self.Add(self.editButton)
		for b in ['platform', 'portal', 'item', 'move', 'draw', 'fill']:
			self.Add(FamilyButton(b, self))
		self.selected = ""
		self.down = False
		self.rect = None
	
	def SetLevel(self, level):
		self.level = level
	
	def ToggleMode(self):
		self.mode = not self.mode
		self.editButton.colors[0] = [100 + 150 * self.mode, 100 + 150 * self.mode, 100 + 150 * self.mode]
	
	def On(self):
		return self.mode and self.level
	
	###
	###	Concurrency events
	###
	
	def Pump(self):
		if self.On():
			Concurrent.Pump(self)
			EventMonitor.Pump(self)	
		else:
			self.editButton.Pump()
	
	def Update(self):
		if self.On():
			Concurrent.Update(self)
		else:
			self.editButton.Update()
	
	def Draw(self):
		if self.On():
			Concurrent.Draw(self)
		else:
			self.editButton.Draw()
	
	###
	###	Interface events
	###
	
	@editOn
	def MouseDown(self, e):
		self.down = True
		if self.selected in ['platform', 'portal', 'item']:
			self.rect = EditBox(e.pos, self.level.camera)
			self.Add(self.rect)
		elif self.selected == 'draw':
			p = [int(x * gfx.width) for x in self.level.camera.FromScreenCoordinates(e.pos)]
			self.level.bitmap.Pixel(p, (150, 150, 150, 255))
	
	@editOn
	def MouseMove(self, e):
		if self.rect:
			self.rect.SetCorner(e.pos)
	
	@editOn
	def MouseUp(self, e):
		self.down = False
		if self.rect:
			self.Remove(self.rect)
			self.rect = None
