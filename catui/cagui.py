#!/usr/bin/env python3

import os
import sys
import re
import crash_session
from optparse import OptionParser

import wx
import wx.html
import wx.xrc
import frame_crash
from ansi2html import Ansi2HTMLConverter


class CrashWindow(frame_crash.FrameCrash):
    full_output = ""

    def __init__(self, parent, options):
        super(CrashWindow, self).__init__(parent)

        if "gtk2" in wx.PlatformInfo:
            self.html_main_output.SetStandardFonts()

        self.ansi_conv = Ansi2HTMLConverter()
        self.catui = crash_session.CrashTUI(self.my_msg_func,
                                            self.html_main_output)
        self.catui.debug_mode = options.verbose_mode


    def OnCharHook_Old(self, event):
        if event.GetEventObject() != self.tc_command_input:
            new_value = self.tc_command_input.GetValue() +\
                    ("%c" % (event.GetUnicodeKey())).lower()
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


    def connect(self, server_name, argument_list=()):
        self.SetTitle("%s" % server_name)
        self.catui.open(server_name, argument_list)


    def run_command(self, command_str):
        self.catui.run(command_str)


    def my_msg_func(self, result_string, private_data=None):
        self.full_output = self.full_output + result_string
        html_window = private_data
        html_window.SetPage(self.ansi_conv.convert(self.full_output))
        html_window.Scroll(-1, self.GetClientSize()[0])


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
