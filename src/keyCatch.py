import wx
 
class MyForm(wx.Frame):
 
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Pacman game", size=(0,0))
 		
		# Add a panel so it looks the correct on all platforms
		panel = wx.Panel(self, wx.ID_ANY)
		btn = wx.TextCtrl(panel, value="")
		btn.SetFocus()
 		
		btn.Bind(wx.EVT_CHAR, self.onCharEvent)

	def onCharEvent(self, event):
		keycode = event.GetKeyCode()
		controlDown = event.CmdDown()
		altDown = event.AltDown()
		shiftDown = event.ShiftDown()
 		
		print keycode
		if keycode == wx.WXK_SPACE:
			print "you pressed the spacebar!"
		elif controlDown and altDown:
			print keycode
		event.Skip()
 
 
# Run the program
if __name__ == "__main__":
	app = wx.PySimpleApp()
	frame = MyForm()
	frame.Show()
	app.MainLoop()
