# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Aug  6 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.html

###########################################################################
## Class FrameCrash
###########################################################################

class FrameCrash ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bs_main = wx.BoxSizer( wx.VERTICAL )

		self.html_main_output = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		bs_main.Add( self.html_main_output, 1, wx.ALL|wx.EXPAND, 5 )

		self.tc_command_input = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bs_main.Add( self.tc_command_input, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bs_main )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CHAR_HOOK, self.OnCharHook )
		self.Bind( wx.EVT_KEY_DOWN, self.FrameCrashOnKeyDown )
		self.tc_command_input.Bind( wx.EVT_TEXT_ENTER, self.OnEnter )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnCharHook( self, event ):
		event.Skip()

	def FrameCrashOnKeyDown( self, event ):
		event.Skip()

	def OnEnter( self, event ):
		event.Skip()



