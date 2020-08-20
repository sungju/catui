# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Aug  6 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.html2

###########################################################################
## Class FrameCrash
###########################################################################

class FrameCrash ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.main_menu = wx.MenuBar( 0 )
		self.file_menu = wx.Menu()
		self.menu_new_session = wx.MenuItem( self.file_menu, wx.ID_ANY, u"New session", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.menu_new_session )

		self.m_menuItem2 = wx.MenuItem( self.file_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.m_menuItem2 )

		self.m_menuItem3 = wx.MenuItem( self.file_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.m_menuItem3 )

		self.main_menu.Append( self.file_menu, u"&File" )

		self.view_menu = wx.Menu()
		self.m_menuItem4 = wx.MenuItem( self.view_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL )
		self.view_menu.Append( self.m_menuItem4 )

		self.m_menuItem5 = wx.MenuItem( self.view_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL )
		self.view_menu.Append( self.m_menuItem5 )

		self.main_menu.Append( self.view_menu, u"&View" )

		self.help_menu = wx.Menu()
		self.m_menuItem6 = wx.MenuItem( self.help_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.m_menuItem6 )

		self.m_menuItem7 = wx.MenuItem( self.help_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.m_menuItem7 )

		self.main_menu.Append( self.help_menu, u"&Help" )

		self.SetMenuBar( self.main_menu )

		bs_main = wx.BoxSizer( wx.VERTICAL )

		self.html_main_output = wx.html2.WebView.New(self, wx.ID_ANY, style=0)
		self.html_main_output.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bs_main.Add( self.html_main_output, 1, wx.ALL|wx.EXPAND, 5 )

		self.tc_command_input = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bs_main.Add( self.tc_command_input, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bs_main )
		self.Layout()
		self.m_main_statusbar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CHAR_HOOK, self.OnCharHook )
		self.Bind( wx.EVT_KEY_DOWN, self.FrameCrashOnKeyDown )
		self.Bind( wx.EVT_MENU, self.OnNewSessionClick, id = self.menu_new_session.GetId() )
		self.html_main_output.Bind( wx.EVT_LEFT_DCLICK, self.OnLeftDClick )
		self.tc_command_input.Bind( wx.EVT_TEXT_ENTER, self.OnEnter )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnCharHook( self, event ):
		event.Skip()

	def FrameCrashOnKeyDown( self, event ):
		event.Skip()

	def OnNewSessionClick( self, event ):
		event.Skip()

	def OnLeftDClick( self, event ):
		event.Skip()

	def OnEnter( self, event ):
		event.Skip()


###########################################################################
## Class DialogServerSelect
###########################################################################

class DialogServerSelect ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 448,296 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Server ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer6.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer6.Add( ( 0, 0), 0, wx.EXPAND, 5 )

		cb_server_listChoices = []
		self.cb_server_list = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, cb_server_listChoices, wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SIMPLE|wx.TE_PROCESS_ENTER )
		bSizer6.Add( self.cb_server_list, 1, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer2.Add( bSizer6, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.tc_details = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
		self.tc_details.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		bSizer12.Add( self.tc_details, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer12, 1, wx.EXPAND, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Arguments ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer9.Add( ( 0, 0), 0, wx.EXPAND, 5 )

		self.tc_options = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.tc_options, 1, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer2.Add( bSizer9, 1, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer10.Add( ( 20, 0), 0, wx.EXPAND, 5 )

		self.btn_ok = wx.Button( self, wx.ID_OK, u"&Ok", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.btn_ok.SetDefault()
		bSizer10.Add( self.btn_ok, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_cancel = wx.Button( self, wx.ID_CANCEL, u"&Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.btn_cancel, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizer10.Add( ( 20, 0), 0, wx.EXPAND, 5 )


		bSizer2.Add( bSizer10, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.cb_server_list.Bind( wx.EVT_COMBOBOX, self.OnServerSelection )
		self.btn_ok.Bind( wx.EVT_BUTTON, self.OnOkClick )
		self.btn_cancel.Bind( wx.EVT_BUTTON, self.OnCancelClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnServerSelection( self, event ):
		event.Skip()

	def OnOkClick( self, event ):
		event.Skip()

	def OnCancelClick( self, event ):
		event.Skip()



