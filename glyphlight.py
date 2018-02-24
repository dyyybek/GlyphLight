#MenuTitle: GlyphLight
# -*- coding: utf-8 -*-
__doc__="""
Spotlight for Glyphs
"""

from AppKit import NSFont, NSColor, NSTextField, NSFocusRingTypeNone
import vanilla
import GlyphsApp
import re
import traceback
import string
import time

class glyphLight(object):

	def __init__(self):
		
		width, height = 600,50

		self.w = vanilla.FloatingWindow((width, height),"")
		self.w.center()


		# Setting Window Appearance

		window = self.w.getNSWindow()
		window.setTitlebarAppearsTransparent_(1) # Hide title bar
		window.setStandardWindowTitleButtonsAlphaValue_(0.00001) # Hiding buttons hack
		window.setBackgroundColor_(NSColor.whiteColor()) # Window background
		window.setAlphaValue_(0.9) # Slight transparency, don't know how to apply vibrancy like in spotlight

		self.w.editText = vanilla.EditText((20, 0, -20, -14), continuous=False, callback=self.test)


		# Setting EditText Appearance

		font = NSFont.systemFontOfSize_weight_(28,-0.5)
		box = self.w.editText.getNSTextField()
		box.setBordered_(False)
		box.setDrawsBackground_(False)
		box.setFont_(font)
		box.setFocusRingType_(NSFocusRingTypeNone)


		# Open window and focus

		self.w.open()
		self.w.select()

		self.w.infoText = vanilla.TextBox((10, -25, -1, -1), "")
		infoBox = self.w.infoText.getNSTextField()
		infoBox.setBordered_(False)
		infoBox.setDrawsBackground_(False)
		# infoBox.setFont_(font)
		infoBox.setFocusRingType_(NSFocusRingTypeNone)

		self.w.line = vanilla.HorizontalLine((10, -56, -10, 0))
		self.w.line.show(0)
		# # self.info.open()
		

	# Clear Input
	def clearInput(self):
		self.w.editText.set("")

	# Matching query to functions

	def callFunction(self, data):
		functionsDict = {"lsb":self.setLSB, "rsb":self.setRSB, "center":self.centerGlyph, "ki":self.switchIncrements, "ki:lo":self.setIncrementsLo, "ki:hi":self.setIncrementsHi, "az":self.tabWithText, "test":self.testprint}
		caller = data.split(' ', 1)[0]
		# print "caller", caller, "data", data
		try:
			if caller in functionsDict.keys():
				doit = functionsDict[caller]
				if len(data.split()) > 1:
					doit(data)
				else:
					doit()
			else:
				self.showInfo("Command not found")

			self.clearInput()

		except:
			print(traceback.format_exc())

	def showInfo(self, message):
		try:
			ps = self.w.getPosSize()
			self.w.infoText.set(message)
			self.w.line.show(1)
			self.w.setPosSize((ps[0],ps[1],ps[2],ps[3]+20), animate=True)			
			time.sleep(1.2)
			self.w.line.show(0)
			self.w.infoText.set("")
			self.w.setPosSize((ps[0],ps[1],ps[2],ps[3]), animate=True)
		except:
			print(traceback.format_exc())

	def test(self, sender):
		data = str(sender.get())
		self.callFunction(data)

	# Tab with text
	def tabWithText(self):
		self.showInfo("Opening a new tab with a-z, A-Z, 0-9")
		font = Glyphs.font
		font.newTab(string.ascii_lowercase + "\n" + string.ascii_uppercase + "\n" + string.digits)

	# Setting LSB
	def setLSB(self, data):
		print "setting LSB"
		font = Glyphs.font
		layer = font.selectedLayers[0]
		num = re.search('\d+', data).group(0)
		num = int(num)
		self.showInfo("Setting LSB to " + str(num))

		if num:
			layer.LSB = num

		

	# Setting LSB
	def setRSB(self, data):
		print "setting RSB"
		font = Glyphs.font
		layer = font.selectedLayers[0]
		num = re.search('\d+', data).group(0)
		num = int(num)
		self.showInfo("Setting RSB to " + str(num))
		
		if num:
			layer.RSB = num


	# Centering glyph
	def centerGlyph(self):
		print "centering glyph"
		self.showInfo("Centering Glyph")
		
		font = Glyphs.font
		layer = font.selectedLayers[0]

		width = layer.width
		LSB = layer.LSB
		RSB = layer.RSB
		
		nSB = (LSB + RSB) / 2.0
		
		layer.LSB = nSB
		layer.width = width


	def setIncrementsLo(self, data):
		print "saving keyboard increments LO"
		self.showInfo("Saving LOW keyboard increments")
		l = re.findall('\d+', data)
		lo = int(l[0])
		hi = int(l[1])
		
		Glyphs.defaults["com.dyb.glyphlight.loSettinglo"] = lo
		Glyphs.defaults["com.dyb.glyphlight.loSettinghi"] = hi
		
	def setIncrementsHi(self, data):
		print "saving keyboard increments HI"
		self.showInfo("Saving HIGH keyboard increments")
		l = re.findall('\d+', data)
		lo = int(l[0])
		hi = int(l[1])

		Glyphs.defaults["com.dyb.glyphlight.hiSettinglo"] = lo
		Glyphs.defaults["com.dyb.glyphlight.hiSettinghi"] = hi


	# Keyboard increments switching ki
	def switchIncrements(self):
		print "changing keyboard increments"

		# There's a fixed setting right now, a method with option to pass own arguments would be nice
		l = [Glyphs.intDefaults["GSKerningIncrementLow"],Glyphs.intDefaults["GSKerningIncrementHigh"],Glyphs.intDefaults["GSSpacingIncrementLow"],Glyphs.intDefaults["GSSpacingIncrementHigh"]]
		try:
			lo = [Glyphs.defaults["com.dyb.glyphlight.loSettinglo"],Glyphs.defaults["com.dyb.glyphlight.loSettinghi"],Glyphs.defaults["com.dyb.glyphlight.loSettinglo"],Glyphs.defaults["com.dyb.glyphlight.loSettinghi"]]
			hi = [Glyphs.defaults["com.dyb.glyphlight.hiSettinglo"],Glyphs.defaults["com.dyb.glyphlight.hiSettinghi"],Glyphs.defaults["com.dyb.glyphlight.hiSettinglo"],Glyphs.defaults["com.dyb.glyphlight.hiSettinghi"]]
		except:
			print(traceback.format_exc())

		if None in lo or None in hi:
			lo = [1,10,1,10]
			hi = [5,20,5,20]
			print "Set your own keyboard increments with ki:lo and ki:hi"
			self.showInfo("Set your own keyboard increments with ki:lo and ki:hi")
		else:
			self.showInfo("Switching keyboard increments")

		# reset if setup is mixed

		if l != lo and l != hi:
			Glyphs.intDefaults["GSKerningIncrementLow"] = None
			Glyphs.intDefaults["GSKerningIncrementHigh"] = None
			Glyphs.intDefaults["GSSpacingIncrementLow"] = None
			Glyphs.intDefaults["GSSpacingIncrementHigh"] = None


		# toggle between lo & hi

		if Glyphs.intDefaults["GSKerningIncrementLow"] == hi[0]:
			Glyphs.intDefaults["GSKerningIncrementLow"] = lo[0]
		elif Glyphs.intDefaults["GSKerningIncrementLow"] == lo[0]:
			Glyphs.intDefaults["GSKerningIncrementLow"] = hi[0]
		else:
			Glyphs.intDefaults["GSKerningIncrementLow"] = None


		if Glyphs.intDefaults["GSKerningIncrementHigh"] == hi[1]:
			Glyphs.intDefaults["GSKerningIncrementHigh"] = lo[1]
		elif Glyphs.intDefaults["GSKerningIncrementHigh"] == lo[1]:
			Glyphs.intDefaults["GSKerningIncrementHigh"] = hi[1]
		else:
			Glyphs.intDefaults["GSKerningIncrementHigh"] = None


		if Glyphs.intDefaults["GSSpacingIncrementLow"] == hi[2]:
			Glyphs.intDefaults["GSSpacingIncrementLow"] = lo[2]
		elif Glyphs.intDefaults["GSSpacingIncrementLow"] == lo[2]:
			Glyphs.intDefaults["GSSpacingIncrementLow"] = hi[2]
		else:
			Glyphs.intDefaults["GSSpacingIncrementLow"] = None


		if Glyphs.intDefaults["GSSpacingIncrementHigh"] == hi[3]:
			Glyphs.intDefaults["GSSpacingIncrementHigh"] = lo[3]
		elif Glyphs.intDefaults["GSSpacingIncrementHigh"] == lo[3]:
			Glyphs.intDefaults["GSSpacingIncrementHigh"] = hi[3]
		else:
			Glyphs.intDefaults["GSSpacingIncrementHigh"] = None
			
	def testprint(self, data):
		print "test successful"


glyphLight()