#!/usr/bin/env python3

import os
import sys
import re
import crash_session
import winlib
import curses
from optparse import OptionParser


def run_and_append(text_viewer, result_string):
    p = re.compile("\^\[\[[0-9;]*m")
    my_string = p.sub('', result_string)

    for line in my_string.splitlines():
        text_viewer.append(line)

    text_viewer.goto_bottom()
    text_viewer.draw_window()


def my_msg_func(result_string, private_data=None):
    tv = private_data
    run_and_append(tv, result_string)


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

    term = winlib.Terminal()
    text_lines = []
    tv = winlib.TextViewer(term, 0, 0, 0, -3, text_lines, 2, 1, normal_color="bright_blue|reverse", draw_now=True)
    tv.goto_top()
    tv.draw_window()

    catui = crash_session.CrashTUI(my_msg_func, tv)
    catui.debug_mode = o.verbose_mode
    '''
    run_and_append(tv, catui.open(args[0], tuple(args[1:])))
    run_and_append(tv, catui.run("bt"))
    run_and_append(tv, catui.run("sys"))
    tv.set_line_type(3)
    run_and_append(tv, catui.run("mod -t"))
    run_and_append(tv, catui.run("kmem -i"))
    '''
    catui.open(args[0], tuple(args[1:]))
    catui.run("bt")

    inp = winlib.InputBox(term, 0, -3, -1, 3, 2, 1)
    while (True):
        result_str, exit_key = inp.get_text("", [curses.KEY_UP, ord('\t'), ord('\n'), 27])
        if exit_key == 27 or result_str.strip() in ["exit", "quit"]:
            break
        catui.run(result_str)

    catui.close()
    #tv.run()


if __name__ == "__main__":
    main()
