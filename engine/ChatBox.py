from PodSix.Resource import *
from PodSix.GUI.TextInput import TextInput
from PodSix.Rectangle import Rectangle

class ChatBox(TextInput):
	def __init__(self, parent):
		self.parent = parent
		# special keys we want to ignore
		self.specials = [8, 9, 13]
		# last mouse position
		self.lastPos = [0, 0]
		# whether to draw this or not
		self.visible = True
		# history of commands we have typed
		self.history = []
		
		TextInput.__init__(self, {"left": 0.01, "bottom": 0.55}, 0.8, "/help", dict([(x, chr(x)) for x in range(97, 122)]), font="chat")
		# remember the drawn rectangle
		self.Draw()
		self.oldRect = self.rect
		self.oldRect[0] -= 4
		self.oldRect[1] -= 4
		self.oldRect[2] += 8
		self.oldRect[3] += 8
		self.oldRect = Rectangle(self.oldRect)
		# remember the original position
		self.oldPos = self.pos
		self.oldText = ""
	
	def Update(self):
		if self.visible:
			TextInput.Update(self)
	
	def Draw(self):
		if self.visible:
			TextInput.Draw(self)
	
	def ShowText(self, text):
		if not self.oldText:
			self.oldText = self.text
		self.text = text
		self.visible = True
	
	def RevertText(self):
		if self.oldText:
			self.text = self.oldText
			self.oldText = ""
		self.visible = False
	
	def KeyDown(self, e):
		if self.visible:
			self.Draw()
			if self.textWidth < self.width * gfx.width  - self.letterWidth and not e.key in self.specials:
				#print e.key
				self.text += e.unicode
	
	def MouseMove(self, e):
		inNew = self.oldRect.PointInRect(e.pos)
		inOld = self.oldRect.PointInRect(self.lastPos)
		# mouse over
		if inNew and not inOld:
			self.visible = True
		# mouse out
		elif inOld and not inNew:
			self.visible = False
		self.lastPos = e.pos[:]

