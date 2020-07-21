#!/usr/bin/env python3

import os
import sys

import pexpect
from pexpect import pxssh
import logging
import re
from optparse import OptionParser

from pathlib import Path


class CrashTUI:
    CRASH_PROMPT = "\ncrash> "
    timeout = 120
    debug_mode = False

    target_list = {}
    child_session = None

    def __init__(self, init_cmd):
        f = None
        try:
            filename = "%s/.catuirc" % str(Path.home())
            f = open(filename, "r")
            lines = f.readlines()
            for line in lines:
                words = line.split('=')
                if words[0].startswith('#'):
                    continue
                if len(words) < 2:
                    continue
                cmd_str = line[line.find('=') + 1:].strip()
                if cmd_str[0] == '\'' or cmd_str[0] == '\"':
                    cmd_str = cmd_str[1:]
                if cmd_str[-1] == '\'' or cmd_str[-1] == '\"':
                    cmd_str = cmd_str[:-1]
                self.target_list[words[0]] = cmd_str
        except Exception as e:
            print(e)
        finally:
            if f is not None:
                f.close()


    def open(self, target, arg_list):
        try:
            if target not in self.target_list:
                print("Target %s is not in the list. Please check ~/.catuirc" % target)
                return

            cmd_str = self.target_list[target]
            cmd_str = cmd_str % arg_list
            cmd_list_all = cmd_str.split("|")
            cmd_list = []
            expect_list = []
            num = 0
            while (num + 1 < len(cmd_list_all)):
                cmd_list.append(cmd_list_all[num])
                num += 1
                expect_list.append(cmd_list_all[num])
                num += 1

            if self.debug_mode:
                print(cmd_list)
                print(expect_list)

            num = 0
            result_str = ""
            while (num < len(cmd_list)):
                result = self.run_one_command(cmd_list[num], expect_list[num])
                result_str = result_str + "\n" + result
                num += 1
            result = self.run_one_command('px 0x499602d2', ' = 0x499602d2\r\ncrash> ')
            result_str = result_str + "\n" + result
            result_str = result_str.replace("px 0x499602d2", "")
            result_lines = result_str.splitlines()
            for i in range(0, len(result_lines) - 2):
                print(result_lines[i])
        except TypeError as e:
            print("Argument list not matching with the target string")
            print(e)
        except Exception as e:
            print(e)
            pass


    def close(self):
        pass


    def run_one_command(self, cmd_str, expect_str):
        result = "<None>"
        try:
            if self.child_session == None:
                if cmd_str.startswith("ssh "):
                    self.child_session = pxssh.pxssh()
                    cmd_list = cmd_str.split()[1].split('@')
                    userinfo = cmd_list[0]
                    if userinfo.find(':') > -1:
                        username, password = userinfo.split(':')
                    else:
                        username = userinfo
                        password = ""
                    hostname = cmd_list[1]
                    self.child_session.login(hostname, username, password)
                else:
                    self.child_session = pexpect.spawn(cmd_str, timeout=self.timeout)
            else:
                if self.debug_mode:
                    print(self.child_session)
                self.child_session.sendline(cmd_str)
                self.child_session.expect(expect_str, timeout=self.timeout)

            result = self.child_session.before.decode("utf-8")
        except Exception as e:
            print(e)

        return result


    def run(self, cmd_str):
        try:
            if self.child_session == None:
                print("Please run crash first")
                return

            self.child_session.sendline(cmd_str)
            result = self.child_session.expect(self.CRASH_PROMPT,
                                               timeout=self.timeout)
            result = self.child_session.before.decode("utf-8")
            print("="* 50)
            print("crash> ", end="")
            for line in result.splitlines():
                print(line)
            print("-" * 50)
        except Exception as e:
            print(e)


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

    catui = CrashTUI("")
    catui.debug_mode = o.verbose_mode
    catui.open(args[0], tuple(args[1:]))
    catui.run("bt")
    catui.run("sys")
    catui.run("mod -t")
    catui.run("kmem -i")
    catui.close()



if __name__ == "__main__":
    main()
