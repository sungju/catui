#!/usr/bin/env python3

import os
import sys

import pexpect
from pexpect import pxssh
import logging
import re
from optparse import OptionParser

from pathlib import Path
import threading
import time


class CrashTUI:
    CRASH_PROMPT = "crash> "
    MAGIC_KEY = "0x499602d2"
    timeout = 60
    debug_mode = False

    target_list = {}
    child_session = None


    def __init__(self, callback_func=None, callback_data=None):
        f = None
        self.callback_func = callback_func
        self.callback_data = callback_data

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

    def __del__(self):
        self.cont_thread = False
        pass


    def msg_deliver(self, message):
        if self.callback_func is None or message is None:
            return

        self.callback_func(message, self.callback_data)

    def is_connected(self):
        return self.child_session != None


    def open(self, target, arg_list):
        result_str = ""
        try:
            if target not in self.target_list:
                result_str = "Target %s is not in the list. Please check ~/.catuirc" % target
                self.msg_deliver(result_str)
                return

            if self.debug_mode:
                print("target: %s" % target)
                print("options : ", arg_list)

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

            num = 0
            while (num < len(cmd_list)):
                result = self.run_one_command(cmd_list[num], expect_list[num])
                result = result + expect_list[num].replace("\\r\\n", "")
                result = result.replace(" unset PROMPT_COMMAND\r\n", "")
                result = result.replace(" PS1='[PEXPECT]\$ '\r\n", "")
                result = result.replace("px %s" % (self.MAGIC_KEY), "")
                result_str = ""
                for line in result.splitlines():
                    result_str = result_str + line + "\n"
                self.msg_deliver(result_str)
                num += 1
            self.run("sf")
        except TypeError as e:
            result_str = result_str + "Argument list not matching with the target string" + "\n"
            result_str = result_str + repr(e) + "\n"
            self.msg_deliver(result_str)
        except Exception as e:
            result_str = result_str + e + "\n"
            self.msg_deliver(result_str)


        return


    def close(self):
        if self.child_session != None:
            self.child_session.close()
            self.child_session = None


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
                    self.child_session.login(hostname, username, password, sync_multiplier=5)
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
            print(self.child_session.before)

        return result


    def run(self, cmd_str):
        result_str = ""
        try:
            if self.child_session == None:
                return "Please run crash first\n"

            if cmd_str != None and len(cmd_str.strip()) > 0:
                cmd_str = cmd_str.strip()
                if cmd_str == "quit" or cmd_str == "exit":
                    self.close()
                    self.msg_deliver("\n%s--- DISCONNECTED ---%s\n" %
                                     (self.MAGIC_KEY, self.MAGIC_KEY))
                    return ""

                self.child_session.sendline(cmd_str)

            result_str = self.run_one_command('px %s' % (self.MAGIC_KEY),
                                              '\$[0-9]+ = %s.*crash> ' % (self.MAGIC_KEY))
            result_str = result_str[:result_str.find("crash> px %s" % (self.MAGIC_KEY))]
            result_str = result_str.replace("px %s" % (self.MAGIC_KEY), "")
            result_lines = result_str.splitlines()
            result_str = ""
            for line in result_lines:
                result_str = result_str + line + "\n"
            result_str = result_str + "crash> "
            self.msg_deliver(result_str)
        except Exception as e:
            print(e)

        return result_str



def callback_func(msg_str, private_data):
    print(msg_str)


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

    catui = CrashTUI(callback_func)
    catui.debug_mode = o.verbose_mode
    catui.open(args[0], tuple(args[1:]))
    catui.run("bt")
    catui.run("sys")
    catui.run("mod -t")
    catui.run("kmem -i")
    catui.close()


if __name__ == "__main__":
    main()
