#!/usr/bin/env python3

import os
import sys
import re
import string
import crash_session
from optparse import OptionParser

import wx
import wx.html
import wx.xrc
import frame_crash
from ansi2html import Ansi2HTMLConverter

class ServerSelectDialog(frame_crash.DialogServerSelect):
    catui = None

    def __init__(self, parent, catui):
        super(ServerSelectDialog, self).__init__(parent)
        self.catui = catui
        first_server = None
        for server in catui.target_list:
            self.cb_server_list.Append(server)
            if first_server is None:
                first_server = server
        if len(catui.target_list) > 0:
            self.cb_server_list.SetSelection(0)
            self.show_arg_list(self.catui.target_list[first_server])


    def OnServerSelection(self, event):
        server = self.cb_server_list.GetValue()
        self.show_arg_list(self.catui.target_list[server])


    def show_arg_list(self, arg_list):
        options = re.findall(r'%s', arg_list)
        self.tc_details.SetValue("%d options needed for the below:\n\n%s" %
                                 (len(options), arg_list))



class CrashWindow(frame_crash.FrameCrash):
    full_output = ""
    debug_mode = False
    options = None

    def __init__(self, parent, options):
        super(CrashWindow, self).__init__(parent)

        if "gtk2" in wx.PlatformInfo:
            self.html_main_output.SetStandardFonts()

        self.options = options
        self.debug_mode = options.verbose_mode
        self.ansi_conv = Ansi2HTMLConverter(inline=True,
                                            font_size="normal",
                                           scheme="xterm")
        self.new_session()



    def new_session(self):
        self.catui = crash_session.CrashTUI(self.my_msg_func,
                                            self.html_main_output)
        self.catui.debug_mode = self.debug_mode


    def OnLeftDClick(self, event):
        # This is for HtmlWindow: Not using for now
        print("OnLeftDClick")
        dc = wx.ClientDC(self.html_main_output)
        pos = event.GetLogicalPosition(dc)
        pos = self.html_main_output.CalcUnscrolledPosition(pos)
        # FIXME: Still line is selected
        self.html_main_output.SelectWord(pos)



    def OnCharHook(self, event):
        key = event.GetUnicodeKey()
        key_char = chr(key)
        if event.GetEventObject() != self.tc_command_input and\
           event.HasAnyModifiers() == False and\
           all(c in string.printable for c in key_char):
            if event.ShiftDown() != True:
                key_char = key_char.lower()

            new_value = self.tc_command_input.GetValue() + key_char
            self.tc_command_input.SetValue(new_value)
            self.tc_command_input.SetFocus()
            self.tc_command_input.SetInsertionPointEnd()
        else:
            event.Skip()


    def OnChar(self, event):
        print("OnChar")
        self.tc_command_input.SetFocus()


    def OnEnter(self, event):
        cmd_str = self.tc_command_input.GetValue()
        self.tc_command_input.SetValue("")
        self.run_command(cmd_str)


    def OnNewSessionClick(self, event):
        try:
            dlg = ServerSelectDialog(None, self.catui)
            if dlg.ShowModal() == wx.ID_OK:
                server = dlg.cb_server_list.GetValue()
                args_str = dlg.tc_options.GetValue().strip()
                if len(args_str) > 0:
                    args = eval(args_str)
                else:
                    args = ()
                cagui = CrashWindow(None, self.options)
                cagui.connect(server, args)
                cagui.Show(True)
            else:
                pass
        finally:
            dlg.Destroy()



    def updateStatusBar(self, text):
        self.m_main_statusbar.SetStatusText(text)
        self.m_main_statusbar.Update()


    def connect(self, server_name, argument_list=()):
        self.SetTitle("%s with %s" % (server_name, str(argument_list)))
        self.updateStatusBar("Connecting to %s" % server_name)
        self.catui.open(server_name, argument_list)
        self.updateStatusBar("Ready")


    def disconnect(self):
        self.catui.close()


    def run_command(self, command_str):
        if self.catui.is_connected() == False:
            self.updateStatusBar("Not connected to any server")
            return

        self.updateStatusBar("Run command '%s'" % command_str)
        self.catui.run(command_str)


    def my_msg_func(self, result_string, private_data=None):
        if self.debug_mode:
            print("<%s>" % result_string)
            #print(":".join("{:02x}".format(ord(c)) for c in result_string))

        if result_string.find(self.catui.MAGIC_KEY) >= 0:
            result_string = result_string.replace(self.catui.MAGIC_KEY, "")
            self.SetTitle("* not connected *")

        self.full_output = self.full_output + result_string
        html_window = private_data
        scroll_str = """
        <body onload='ScrollToBottom()' ondblclick='CopyToClipboard()'>
        <script>
        function ScrollToBottom() {
            window.scrollTo(0, document.body.scrollHeight);
        }
        function CopyToClipboard() {
            document.execCommand('copy');
        }
        </script>
        """
        html_window.SetPage(self.ansi_conv.convert(self.full_output) + scroll_str, "")
        #r = html_window.GetScrollRange(wx.VERTICAL)
        #html_window.Scroll(0, r)


def main():
    usage_str = "Usage) %prog <options> target [extra arguments]"
    desc_str = "Example: %prog galvatron 448038195"
    op = OptionParser(usage=usage_str, description=desc_str)
    op.add_option('-v', '--verbose', dest='verbose_mode',
                  default=False, action="store_true",
                  help="Shows debugging messages")

    (o, args) = op.parse_args()
    if len(args) == 0:
        op.print_help()
        sys.exit(-1)

    app = wx.App(False)
    cagui = CrashWindow(None, o)
    cagui.connect(args[0], tuple(args[1:]))
    cagui.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
