#!/usr/bin/env python

import os
import signal
import curses


class Terminal:
    stdscr = 0
    max_colors = 0

    def __init__(self):
        self.init_window()


    def disable_cursor(self):
        curses.cbreak()
        curses.curs_set(0)


    def enable_cursor(self):
        curses.curs_set(1)


    def init_window(self):
        try:
            os.environ['ESCDELAY']
        except KeyError:
            os.environ['ESCDELAY'] = '25'
        self.stdscr = curses.initscr()
        self.disable_cursor()
        curses.noecho()
        self.stdscr.keypad(1)
        curses.start_color()
        curses.use_default_colors()
        self.max_colors = curses.COLORS
        for i in range(0, self.max_colors):
            curses.init_pair(i + 1, i, -1)


    def __del__(self):
        self.stdscr.getkey()
        self.stdscr.keypad(0)
        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()



class SKColor:
    normal_color = "white"
    reverse_color = False
    bold_color = False
    blink_color = False

    color_list = {
        "black": 1,
        "red": 2,
        "green": 3,
        "yellow": 4,
        "blue": 5,
        "magenta": 6,
        "cyan": 7,
        "white": 8,
        "bright_black": 9,
        "bright_red": 10,
        "bright_green": 11,
        "bright_yellow": 12,
        "bright_blue": 13,
        "bright_magenta": 14,
        "bright_cyan": 15,
        "bright_white": 16,
    }

    def __init__(self, normal_color):
        self.normal_color, self.reverse_color, self.bold_color, self.blink_color = self.parse_color(normal_color)


    def parse_color(self, color_str):
        words = color_str.split("|")
        reverse_color = False
        bold_color = False
        blink_color = False

        for word in words:
            word = word.strip().lower()
            if word == "reverse":
                reverse_color = True
            if word == "bold":
                bold_color = True
            if word == "blink":
                blink_color = True

        normal_color = ""
        if words[0].strip() in self.color_list:
            normal_color = words[0].strip()

        return normal_color, reverse_color, bold_color, blink_color


    def get_attrs(self, reverse_color, bold_color, blink_color):
        attrs = 0
        if reverse_color:
            attrs = attrs | curses.A_REVERSE
        if bold_color:
            attrs = attrs | curses.A_BOLD
        if blink_color:
            attrs = attrs | curses.A_BLINK

        return attrs

    def get_cur_attrs(self):
        return self.get_attrs(self.reverse_color, self.bold_color, self.blink_color)


    def get_cur_color(self):
        return curses.color_pair(self.color_list[self.normal_color]) | self.get_cur_attrs()


    def get_color(self, color_str):
        color_str, reverse_color, bold_color, blink_color = self.parse_color(color_str)
        if color_str not in self.color_list:
            return 0
        return curses.color_pair(self.color_list[color_str]) | self.get_attrs(reverse_color,
                                                           bold_color, blink_color)


    def get_cur_color_str(self):
        return self.normal_color


    def get_cur_reverse_color(self):
        attrs = self.get_cur_attrs()
        attrs = attrs ^ curses.A_REVERSE
        return curses.color_pair(self.color_list[self.normal_color]) | attrs


    def get_reverse_color(self, color_str):
        if color_str not in self.color_list:
            return 0
        return curses.color_pair(self.color_list[color_str]) | curses.A_REVERSE



class SKWindow:
    term = None
    screen = None
    pos = (0, 0)
    screen_pos = (0, 0)
    cur_color = None

    x = 0
    y = 0
    maxx = 0
    maxy = 0
    width = 0
    height = 0

    padx = 0
    pady = 0

    def __init__(self, term, x, y, width, height, padx=0, pady=0):
        self.term = term
        self.screen = term.stdscr
        self.cur_color = SKColor("white")
        (smaxy, smaxx) = self.screen.getmaxyx()
        if x < 0:
            x = smaxx + x
        if y < 0:
            y = smaxy + y
        self.x = x
        self.y = y

        if width <= 0:
            width = smaxx - x + width
        if height <= 0:
            height = smaxy - y + height

        if (x + width - 1) > smaxx:
            width = smaxx - x
        if (y + height - 1) > smaxy:
            height = smaxy - y

        self.width = width
        self.height = height
        self.maxx = x + width - 1
        self.maxy = y + height - 1

        self.padx = padx
        self.pady = pady


    def move(self, x, y):
        (smaxy, smaxx) = self.screen.getmaxyx()
        if x + self.width > smaxx:
            x = smaxx - self.width
        if y + self.height > smaxy:
            y = smaxy - self.height

        self.x = x
        self.y = y


    def save_window_area(self, x, y, width, height):
        saved_data = []
        if (x + width) > self.width or (y + height) > self.height:
            return saved_data

        if x > self.width or y > self.height:
            return saved_data

        x = self.x + x
        y = self.y + y

        for ypos in range(0, height):
            saved_row = []
            for xpos in range(0, width):
                saved_row.append(self.screen.inch(y + ypos, x + xpos))
            saved_data.append(saved_row)

        return saved_data


    def save_window(self):
        return self.save_window_area(0, 0, self.width, self.height)


    def restore_window_area(self, x, y, saved_data):
        if x > self.width or y > self.height:
            return

        ypos = 0
        for row in saved_data:
            if y + ypos >= self.height:
                break
            xpos = 0
            for column in row:
                if x + xpos >= self.width:
                    break
                self.screen.delch(self.y + y + ypos, self.x + x + xpos)
                self.screen.insch(self.y + y + ypos, self.x + x + xpos, column)
                xpos = xpos + 1
            ypos = ypos + 1


    def restore_window(self, saved_data):
        self.restore_window_area(0, 0, saved_data)


    def print(self, str, color=-1):
        x, y = self.screen_pos
        if color == -1:
            color = self.cur_color.get_cur_color()
        self.screen.addstr(y, x, str, color)


    def movexy(self, x, y):
        if x > self.width or y > self.height:
            return self.pos
        self.screen_pos = (self.x + x, self.y + y)
        self.pos = (x, y)
        self.screen.move(self.y + y, self.x + x)
        return self.pos


    def get_pad_xy(self, padx, pady):
        if padx == -1:
            padx = self.padx
        if pady == -1:
            pady = self.pady

        return padx, pady


    def printstr(self, str, padx=-1, pady=-1, color=-1):
        cur_x, cur_y = self.pos
        padx, pady = self.get_pad_xy(padx, pady)

        if cur_x + len(str) > (self.width - padx):
            str = str[:(self.width - padx) - cur_x]
        if color == -1:
            color = self.cur_color.get_cur_color()
        self.print(str, color)


    def printxy(self, x, y, str, padx=-1, pady=-1, color=-1):
        padx, pady = self.get_pad_xy(padx, pady)

        y += pady
        if y >= (self.height - pady):
            return
        x += padx
        self.movexy(x, y)
        if color == -1:
            color = self.cur_color.get_cur_color()
        self.printstr(str, padx, pady, color)


    def wprintxy(self, y, str, color=-1):
        padx, pady = self.get_pad_xy(-1, -1)
        y += pady - 1
        if y >= (self.height - pady):
            return
        str = "{0:{align}{width}}".format(str, align="<", width=(self.width - padx * 2))
        if color == -1:
            color = self.cur_color.get_cur_color()
        self.printxy(0, y, str, color=color)


    key_list = {
        27: 'key_escape',
        10: 'key_enter',
        curses.KEY_LEFT: 'key_left',
        curses.KEY_RIGHT: 'key_right',
        curses.KEY_UP: 'key_up',
        curses.KEY_DOWN: 'key_down',
    }

    def get_key_str(self, key_code):
        if key_code in self.key_list:
            return self.key_list[key_code]

        return "unknown"


class BoxWindow(SKWindow):
    bg_type = 0
    line_type = 0
    line_shape = {
        0: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        1: ['┌', '─', '┐', '│', '│', '└', '─', '┘'],
        2: ['╔', '═', '╗', '║', '║', '╚', '═', '╝'],
        3: ['+', '-', '+', '|', '|', '+', '-', '+'],
        4: ['*', '=', '*', '|', '|', '*', '=', '+'],
    }
    bg_shape = {
        0: ' ', 1: '░', 2: '▒', 3: '▓', 4: '█',
        5: '≡',
    }

    def __init__(self, term, x, y, width, height, line_type,
                 bg_type=0, normal_color="white", draw_now=True):
        super(BoxWindow, self).__init__(term, x, y, width, height, 1, 1)
        self.cur_color = SKColor(normal_color)
        if bg_type in self.bg_shape:
            self.bg_type = bg_type
        else:
            bg_type = 0
        self.line_type = line_type
        if draw_now == True:
            self.clear_box(x, y, width, height, 0, 0, color=-1)
        if line_type > 0 and draw_now == True:
            self.draw_box()


    def refresh(self):
        self.screen.refresh()


    def clear_box(self, x=-1, y=-1, width=-1, height=-1, padx=-1, pady=-1, color=-1):
        if x == -1:
            x = self.x
        if y == -1:
            y = self.y
        if width == -1:
            width = self.width
        if height == -1:
            height = self.height
        if color == -1:
            color = self.cur_color.get_cur_color()
        if color == -2:
            color = self.cur_color.get_cur_reverse_color()
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.printxy(x, y, self.bg_shape[self.bg_type],
                             padx, pady, color)



    def set_line_type(self, line_type):
        self.line_type = line_type
        self.draw_box()


    def draw_box(self):
        if not self.draw_box:
            return

        if self.line_type == 0:
            return

        if self.line_type not in self.line_shape:
            return
        line_shape = self.line_shape[self.line_type]
        self.printxy(0, 0, line_shape[0], padx=0, pady=0)
        self.printxy(0, self.height - 1, line_shape[5],
                    padx=0, pady=0)
        for i in range(1, self.width -1):
            self.printxy(i, 0, line_shape[1], padx=0, pady=0)
            self.printxy(i, self.height - 1, line_shape[6],
                         padx=0, pady=0)

        self.printxy(self.width - 1, 0, line_shape[2],
                    padx=0, pady=0)
        self.printxy(self.width - 1, self.height - 1, line_shape[7],
                    padx=0, pady=0)
        for i in range(1, self.height - 1):
            self.printxy(0, i, line_shape[3], padx=0, pady=0)
            self.printxy(self.width - 1, i, line_shape[4],
                        padx=0, pady=0)


class ListItem:
    message = ""
    call_func = None
    private_data = None

    def __init__(self, message, call_func, private_data):
        self.message = message
        self.call_func = call_func
        self.private_data = private_data


    def get_message(self):
        return self.message


    def get_call_func(self):
        return self.call_func


    def get_private_data(self):
        return self.private_data


    def execute_call_func(self):
        if self.call_func is None:
            return -1

        return self.call_func(self.message, self.private_data)



class TextViewer(BoxWindow):
    text_lines = []
    xpos = 0
    ypos = 0

    def __init__(self, term, x, y, width, height, text_lines,
                 line_type, bg_type=0, normal_color="white", draw_now=False):
        super(TextViewer, self).__init__(term, x, y, width, height,
                                        line_type, bg_type, normal_color, draw_now)

        self.text_lines = text_lines


    def append(self, new_string):
        if self.text_lines is None:
            return

        self.text_lines.append(new_string)


    def draw_window(self):
        for i in range(0, self.height):
            text_pos = self.ypos + i
            if (text_pos >= len(self.text_lines)):
                text_msg = " "
            else:
                text_msg = self.text_lines[text_pos]
                if len(text_msg) < self.xpos:
                    text_msg = ""
                else:
                    text_msg = text_msg[self.xpos:]

            '''
            if text_msg == "":
                text_msg = ""
            '''

            self.wprintxy(i, text_msg)
        self.refresh()


    def goto_top(self):
        self.ypos = 0


    def goto_up(self):
        self.ypos = self.ypos - 1
        if self.ypos < 0:
            self.ypos = 0


    def goto_bottom(self):
        last_page = len(self.text_lines) - (self.height - self.pady * 2)
        if last_page < 0:
            last_page = 0

        self.ypos = last_page


    def goto_down(self):
        self.ypos = self.ypos + 1
        last_page = len(self.text_lines) - (self.height - self.pady * 2)
        if last_page < 0:
            last_page = 0

        if self.ypos > last_page:
            self.ypos = last_page


    def goto_left_boundary(self):
        self.xpos = 0


    def goto_left(self):
        self.xpos = self.xpos - 1
        if self.xpos < 0:
            self.xpos = 0


    def get_max_width(self):
        max_width = self.width
        for i in self.text_lines:
            if len(i) > max_width:
                max_width = len(i)

        return max_width


    def get_last_width(self):
        max_width = self.get_max_width()

        last_width = max_width - (self.width - self.padx * 2)
        if last_width < 0:
            last_width = 0

        return last_width


    def goto_right_boundary(self):
        last_width = self.get_last_width()

        self.xpos = last_width


    def goto_right(self):
        last_width = self.get_last_width()
        self.xpos = self.xpos + 1
        if self.xpos > last_width:
            self.xpos = last_width


    def run(self, exit_keys=[]):
        if self.text_lines is None or len(self.text_lines) == 0:
            return
        max_width = self.get_max_width() - 1

        x_percent = y_percent = 1
        x_scale = float(max_width) / (self.width - self.padx * 2)
        y_scale = float(len(self.text_lines)) / (self.height - self.pady * 2)
        if x_scale == 0.0:
            x_scale = 1.0
        if y_scale == 0.0:
            y_scale = 1.0


        last_page = len(self.text_lines) - (self.height - self.pady * 2)
        if last_page < 0:
            last_page = len(self.text_lines) - 1

        while True:
            self.draw_window()
            self.printxy(x_percent, self.height - 1,
                         self.line_shape[self.line_type][6], 0, 0)
            self.printxy(self.width - 1, y_percent,
                         self.line_shape[self.line_type][4], 0, 0)
            x_percent = int(self.xpos / x_scale) + 1
            y_percent = int(self.ypos / y_scale) + 1
            self.printxy(x_percent, self.height - 1, '#', 0, 0)
            self.printxy(self.width - 1, y_percent, '#', 0, 0)
            ch = self.screen.getch()
            if ch in exit_keys:
                break # exit if there's a matching key in the list

            if ch == curses.KEY_UP:
                self.goto_up()
            elif ch == curses.KEY_PPAGE:
                for i in range(0, self.height - self.pady * 2):
                    self.goto_up()
            elif ch == curses.KEY_DOWN:
                self.goto_down()
            elif ch == 0x20 or ch == curses.KEY_NPAGE:
                for i in range(0, self.height - self.pady * 2):
                    self.goto_down()
            elif ch == curses.KEY_LEFT:
                self.goto_left()
            elif ch == curses.KEY_RIGHT:
                self.goto_right()
            elif ch == 27:
                break
            else:
                pass



class ListBox(BoxWindow):
    item_list = []
    cur_item = 0
    cur_top = 0
    cur_xpos = 0
    max_xpos = 0
    max_width = 0
    sel_color = 0
    view_only = False

    def __init__(self, term, x, y, width, height, item_list,
                 line_type, bg_type=0, normal_color="white", draw_now=True, view_only=False):
        super(ListBox, self).__init__(term, x, y, width, height,
                                      line_type, bg_type, normal_color, draw_now=False)
        self.view_only = view_only
        (smaxy, smaxx) = self.screen.getmaxyx()

        max_width = 0
        for item in item_list:
            if len(item.message) > max_width:
                max_width = len(item.message)

        self.max_width = max_width

        if width == -1:
            self.width = max_width + self.padx * 2

        if height == -1:
            self.height = len(item_list) + self.pady * 2

        if (self.x + self.width) >= smaxx:
            self.width = smaxx - self.x
        if (self.y + self.height) >= smaxy:
            self.height = smaxy - self.y

        self.max_xpos = self.max_width - self.width + (self.padx * 2)
        if self.max_xpos < 0:
            self.max_xpos = 0

        self.sel_color = SKColor(normal_color)
        self.item_list = item_list

        if draw_now == True:
            self.clear_box()
            self.draw_box()
            self.draw_items(True)


    def draw_items(self, clear_bg=False):
        y = 0
        max_idx = self.cur_top + \
                min(len(self.item_list) - self.cur_top,
                    self.height - (self.pady * 2))
        sel_color = self.cur_color.get_cur_reverse_color()
        normal_color = self.cur_color.get_cur_color()
        if clear_bg == True:
            self.clear_box(0, 0,
                           self.width - (self.padx * 2),
                           self.height - (self.pady * 2), sel_color)
            self.draw_box()
        for pos in range(self.cur_top, max_idx):
            message = self.item_list[pos].message
            if len(message) > self.cur_xpos:
                message = message[self.cur_xpos:]
            else:
                message = ""
            if pos == self.cur_item:
                self.wprintxy(y, message, sel_color)
            else:
                self.wprintxy(y, message, normal_color)
            y += 1

        self.screen.refresh()


    def draw_pos(self, idx, char):
        item_count = len(self.item_list) - 1
        height = self.height - (self.pady * 2)
        if item_count >= height:
            pos = min(round(idx / item_count * height), height - 1)
            self.printxy(self.width - 1, self.pady + pos, char, 0, 0)

        if self.view_only == False or self.max_width <= self.width:
            return

        width = self.width - (self.padx * 2)
        if self.max_width >= width:
            max_width = self.max_width - width
            if max_width <= 0:
                max_width = width
            pos = min(round(self.cur_xpos / max_width * width), width - 1)
            self.printxy(self.padx + pos, self.height - 1, char, 0, 0)


    def select_item(self, idx):
        item_count = len(self.item_list) - 1
        if idx > item_count:
            return

        self.draw_pos(self.cur_item, self.line_shape[self.line_type][4])
        height = self.height - (self.pady * 2)
        if self.cur_top > idx:
            self.cur_top = idx
        elif idx - self.cur_top >= height:
            self.cur_top = idx - height + 1

        if idx == item_count and item_count > height:
            self.cur_top = idx - height + 1

        self.cur_item = idx
        self.draw_items()

        self.draw_pos(self.cur_item, '#')


    def run(self, exit_keys=['key_escape']):
        item_count = len(self.item_list) - 1
        val = ''
        while val not in exit_keys:
            inp = self.screen.getch()
            val = self.get_key_str(inp)
            if val == 'key_up':
                if self.cur_item > 0:
                    self.select_item(self.cur_item - 1)
                elif self.view_only == False:
                    self.select_item(item_count)
                else:
                    pass
            elif val == 'key_down':
                if self.cur_item < item_count:
                    self.select_item(self.cur_item + 1)
                elif self.view_only == False:
                    self.select_item(0)
                else:
                    pass
            elif val == 'key_enter':
                item = self.item_list[self.cur_item]
                if item.call_func is not None:
                    val = item.call_func(item.private_data)
                    if val == "exit_menu":
                        return "key_enter"
            elif self.view_only:
                if val == 'key_left':
                    self.draw_items()
                    self.draw_pos(self.cur_item, self.line_shape[self.line_type][6])

                    if self.cur_xpos > 0:
                        self.cur_xpos -= 1

                    self.draw_items()
                    self.draw_pos(self.cur_item, '#')
                    val = ''
                elif val == 'key_right':
                    self.draw_items()
                    self.draw_pos(self.cur_item, self.line_shape[self.line_type][6])

                    if self.cur_xpos < self.max_xpos:
                        self.cur_xpos += 1

                    self.draw_items()
                    self.draw_pos(self.cur_item, '#')
                    val = ''
                else:
                    pass
            else:
                pass

        return val


class PulldownMenu(BoxWindow):
    menu_list = []
    cur_item = 0
    saved_data = []

    def __init__(self, term, x, y, width, height, menu_list,
                 bg_type=0, normal_color="white"):
        super(PulldownMenu, self).__init__(term, x, y, width, height,
                                           0, bg_type, normal_color)

        self.saved_data = self.save_window()
        self.menu_list = menu_list
        self.clear_box(padx=0, pady=0, color=-2)
        self.draw_items(False)
        self.select_item(2)
        self.draw_items()


    def draw_items(self, draw_sub=True):
        xpos = self.x + 1
        ypos = self.y
        sel_color = self.cur_color.get_cur_color()
        normal_color = self.cur_color.get_cur_reverse_color()

        sel_menu = None
        for idx in self.menu_list:
            item = self.menu_list[idx]
            message = item['item'].message
            menu = item['menu']
            menu.move(xpos, ypos + 1)
            if idx == self.cur_item:
                self.printxy(xpos, ypos, message, padx=0, pady=0, color=sel_color)
                sel_menu = menu
            else:
                self.printxy(xpos, ypos, message, padx=0, pady=0, color=normal_color)

            item['xpos'] = xpos
            item['ypos'] = ypos

            xpos = xpos + len(message) + 2
            idx += 1

        if draw_sub == True:
            sel_menu.draw_items(True)


    def restore_cur_window(self):
        prev_item = self.menu_list[self.cur_item]
        if "saved_data" in prev_item:
            data = prev_item['saved_data']
            prev_item["menu"].restore_window(data)
            prev_item['saved_data'] = None
            del data[:]
            del data


    def save_cur_window(self):
        cur_item = self.menu_list[self.cur_item]
        cur_item['saved_data'] = cur_item['menu'].save_window()


    def select_item(self, idx):
        self.restore_cur_window()
        self.cur_item = idx
        self.save_cur_window()
        self.draw_items()


    def run(self, exit_keys=['key_escape', 'key_enter'], restore=False):
        item_count = len(self.menu_list) - 1
        val = ''
        sub_menu = None
        while val not in exit_keys:
            sub_menu = self.menu_list[self.cur_item]
            val = sub_menu['menu'].run(exit_keys=['key_escape', 'key_left', 'key_right'])
            if val == 'key_left':
                if self.cur_item > 0:
                    self.select_item(self.cur_item - 1)
                else:
                    self.select_item(item_count)
            elif val == 'key_right':
                if self.cur_item < item_count:
                    self.select_item(self.cur_item + 1)
                else:
                    self.select_item(0)
            else:
                pass

        self.restore_cur_window()
        if restore == True:
            self.restore_window(self.saved_data)

        return val


class InputBox(BoxWindow):

    def __init__(self, term, x, y, width, height, line_type,
                 bg_type=0, normal_color="white", draw_now=True):
        super(InputBox, self).__init__(term, x, y, width, height,
                                       line_type, bg_type, normal_color,
                                       draw_now)


    def get_text(self, initial_str="", exit_keys=[]):
        result_str = initial_str
        ch = ''
        pos = len(result_str)
        insmod = True

        self.term.enable_cursor()

        while (True):
            self.wprintxy(0, result_str)
            self.movexy(pos + self.padx, 0 + self.pady)
            ch = self.screen.getch()
            if ch in exit_keys:
                break
            elif ch in [curses.KEY_BACKSPACE, 127, 330]:
                pos = pos - 1
                if pos < 0:
                    pos = 0
                result_str = result_str[:pos] + result_str[pos + 1:]
            elif ch == curses.KEY_LEFT:
                pos = pos - 1
                if pos < 0:
                    pos = 0
            elif ch == curses.KEY_RIGHT:
                pos = pos + 1
                if pos > len(result_str):
                    pos = len(result_str)
            elif ("%c" % ch).isprintable():
                if pos >= len(result_str):
                    result_str = result_str + "%c" % ch
                    pos = pos + 1
                else:
                    if insmod == True:
                        result_str = result_str[:pos] + ("%c" % ch) + result_str[pos:]
                    else:
                        result_str = result_str[:pos] + ("%c" % ch) + result_str[pos + 1:]
                    pos = pos + 1


        self.term.disable_cursor()

        return result_str, ch


class DialogBox(BoxWindow):
    def __init__(self):
        pass


    def dialog_msg(self, screen, x, y, width, height, color,
                title, msg, menu_list):
        saved_data = self.save_window(screen, x, y, width, height)

        self.fill_box(screen, x, y, width, height, color)
        screen.addstr(y, x + width / 2 - len(title) / 2,
                    title, color | curses.A_REVERSE)
        msg_list = msg.split('\n')
        count = 1
        for msg_str in msg_list:
            screen.addstr(y + count, x + width / 2 - len(msg_str) / 2,
                        msg_str, color | curses.A_REVERSE)
            count = count + 1

        selected_item = self.vmenu(screen, x + 1, y + 3, width - 2, menu_list,
                            curses.color_pair(10), curses.color_pair(8))
        self.restore_window(screen, x, y, saved_data)

        return selected_item




# Unit Test routines
def my_callback_func(private_data):
    box = private_data['box']
    box.printxy(0, 0, "%s" % private_data['message'])
    return "exit_menu"


def my_callback_func_int(private_data):
    box = private_data['box']
    box.printxy(0, 1, "%d" % private_data['number'])
    return "key_enter"


def unit_test():
    global box
    term = Terminal()
    '''
    box = BoxWindow(term, 5, 15, 40, 5, 3, 1, normal_color="bright_white")


    callback_data_str1 = {'box': box, 'message': 'Hello'}
    callback_data_str2 = {'box': box, 'message': 'Wow'}
    callback_data_str3 = {'box': box, 'message': 'Good'}

    callback_data_no1 = {'box': box, 'number': 50}
    callback_data_no2 = {'box': box, 'number': 2390}
    callback_data_no3 = {'box': box, 'number': 12798}
    item_list = [
        ListItem(" First menu is the best ", my_callback_func, callback_data_str1),
        ListItem(" Second ", my_callback_func, callback_data_str2),
        ListItem(" Third ", my_callback_func, callback_data_str3),
        ListItem(" Fourth ", my_callback_func_int, callback_data_no1),
        ListItem(" Fifth ", my_callback_func_int, callback_data_no2),
        ListItem(" Sixth ", my_callback_func_int, callback_data_no3),
        ListItem(" Seventh ", None, None),
        ListItem(" Eighth ", None, None),
        ListItem(" Nineth ", None, None),
    ]
    box.printxy(0, 0, "%d" % (len(item_list)))
    term.stdscr.getkey()

    box4 = ListBox(term, 10, 9, -1, 7, item_list,
                   3, 0, normal_color="cyan|reverse|bold", view_only=True)
    exit_keys = ['key_escape', 'key_enter', 'key_left', 'key_right']
    box4.print(box4.run(exit_keys))
    data = box4.save_window()
    box4.printxy(15, 5, "Merong")
    box4.printxy(15, 6, "%x" % (data[0][0]))
    box4.printxy(15, 6, "%x" % (data[0][0] & 0xff))
    term.stdscr.getkey()
    box4.restore_window_area(0, 0, data)


    menu_list = {
        0: {"item": ListItem(" File ", None, None),
            "menu": ListBox(term, 0, 0, -1, -1,
                            item_list, 3, 0, normal_color="green", draw_now=False),
            },
        1: {"item": ListItem(" Edit ", None, None),
            "menu": ListBox(term, 10, 0, -1, -1,
                            item_list, 3, 0, normal_color="green", draw_now=False),
        },
        2: {"item": ListItem(" View ", None, None),
            "menu": ListBox(term, 20, 0, -1, -1,
                            item_list, 3, 0, normal_color="green", draw_now=False),
        },
    }

    box5 = PulldownMenu(term, 0, 0, -1, 1, menu_list, 0, normal_color="green")
    val = box5.run(restore=True)
    box.printxy(1, 1, "<%s> pressed" % val)


    f = open("winlib.py", "r")
    #f = open("../README.md", "r")
    text_lines = f.readlines()
    tv = TextViewer(term, 0, 0, 70, 25, text_lines, 2, 1, normal_color="bright_blue|reverse", draw_now=True)
    tv.goto_bottom()
    tv.draw_window()
    term.stdscr.getkey()
    text_lines.append("I am a new line\n")
    tv.goto_bottom()
    tv.goto_right_boundary()
    for i in range(1, 10):
        tv.goto_left()
    tv.draw_window()
    tv.run(exit_keys=[curses.KEY_UP, curses.KEY_DOWN])
    '''


    inp = InputBox(term, 0, -3, -1, 3, 2, 1)
    result_str, a = inp.get_text("", [curses.KEY_UP, ord('\t'), ord('\n'), 27])
    inp.printxy(0, 0, "Key %d pressed" % a)

    #term.stdscr.getkey()


if __name__ == "__main__":
    unit_test()
