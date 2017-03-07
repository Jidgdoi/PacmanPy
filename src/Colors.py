# -*- coding:utf-8 -*-

# Cyril Fournier
# 03/27/2015

class color():
	"""
	Print a colored text to the terminal.
	"""
	def __init__(self, fgColor='', bgColor='', fgLight=False, bgLight=False, bold=False, underline=False, italic=False):
		for i in ["fgColor", "bgColor", "fgLight", "bgLight", "bold", "underline", "italic"]:
			cmd = "self.%s = %s" %(i, i)
			exec(cmd)
		self._updateMyFont()

	def __call__(self, text):
		"""
		This function is called when you call an object color as a function.
		e.g.: blue = color(fg='blue')
			  print blue("Hello world.")
		"""
		return self.myFont + str(text) + reset()

	def __repr__(self):
		"""
		This function is called when the object is printed.
		"""
		txt = "fgColor: %s\tbgColor: %s\tbold: %s\titalic: %s\nfgLight: %s\tbgLight: %s\tunderline: %s" %(self.fgColor, self.bgColor, self.bold, self.italic, self.fgLight, self.bgLight, self.underline)
		txt = "fgColor\tbgColor\tbold\titalic\tfgLight\tbgLight\tunderline\n" +\
			  "%s\t%s\t%s\t%s\t%s\t%s\t%s" %(self.fgColor, self.bgColor, self.bold, self.italic, self.fgLight, self.bgLight, self.underline)
		return txt

	def _updateMyFont(self):
		"""
		Update the myFont variable.
		"""
		self.myFont = buildColor(self.fgColor, self.bgColor, self.fgLight, self.bgLight, self.bold, self.underline, self.italic)

	def setColor(self, fgColor='', bgColor='', fgLight='', bgLight='', bold='', underline='', italic=''):
		"""
		Set new value for the parameter.
		"""
		args = locals().keys()
		args.remove('self')
		for i in args:
			cmd = "if %s != '': self.%s = %s" %(i, i, i)
			exec(cmd)
		self._updateMyFont()

# ------------------------------------
# --- Building and drawing functions
# ------------------------------------

def draw(text, fgColor='', bgColor='', fgLight=False, bgLight=False, bold=False, underline=False, italic=False):
	"""
	Return the text surrounded by color prompt syntax.
	"Color|Text|Reset"
	e.g.: "\033[1;94mHello world.\033[0m"
	"""
	colorSyntax = buildColor(fgColor, bgColor, fgLight, bgLight, bold, underline, italic)
	return colorSyntax + str(text) + reset()

def buildColor(fgColor='', bgColor='', fgLight=False, bgLight=False, bold=False, underline=False, italic=False):
	"""
	Return the wanted color and style in "color bash prompt" format.
	To get a reset color, run this function without arguments or run the reset() function.
	"""
	struct = "\033["
	dColors = {'black':'0', 'red':'1', 'green':'2', 'yellow':'3', 'blue':'4', 'purple':'5', 'cyan':'6', 'white':'7', 'k':'0', 'r':'1', 'g':'2', 'y':'3', 'b':'4', 'p':'5', 'c':'6', 'w':'7', '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7'}
	styles = {'bold':'1', 'underline':'2', 'italic':'3'}
	
	# --- Set style
	st = []
	if bold:
		st.append(styles['bold'])
	if underline:
		st.append(styles['underline'])
	if italic:
		st.append(styles['italic'])
	st = ';'.join(st) or '0'
	
	# --- Set foreground
	fg = ''
	if fgColor.lower() in dColors:
		if fgLight: fg = '9'
		else:		fg = '3'
		fg += dColors[fgColor.lower()]
	elif fgColor != '':
		print warning("Warning: the value '%s' isn't a valid color." %fgColor)
	
	# --- Set background
	bg = ''
	if bgColor in dColors:
		if bgLight: bg = '10'
		else:		bg = '4'
		bg += dColors[bgColor]
	elif bgColor != '':
		print warning("Warning: the value '%s' isn't a valid color." %fgColor)
	
	# --- Merge results
	res = struct + st
	if fg: res += ";%s" %fg
	if bg: res += ";%s" %bg
	res += "m"
	return res

def reset():
	"""
	Reset the text color.
	"""
	return "\033[0m"

# ------------------------------------
# --- Prebuilt colored functions
# ------------------------------------

def error(text):
	"""
	Return the text in an 'error format', i.e. red and bold.
	"""
	return draw(text, fgColor='red', bold=True)

def warning(text):
	"""
	Return the text in a 'warning format', i.e. yellow and bold.
	"""
	return draw(text, fgColor='yellow', bold=True)

def success(text):
	"""
	Return the text in a 'success format', i.e. green and bold.
	"""
	return draw(text, fgColor='green', bold=True)

def comment(text):
	"""
	Return the text in python commentary format.
	e.g., # text (in dark blue and italic)
	"""
	return draw('# %s' %text, fgColor='blue', italic=True)
