"""
This type stub file was generated by pyright.
"""

'''
This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
'''
CSI = '\033['
OSC = '\033]'
BEL = '\007'
def code_to_chars(code):
    ...

def set_title(title):
    ...

def clear_screen(mode=...):
    ...

def clear_line(mode=...):
    ...

class AnsiCodes(object):
    def __init__(self):
        ...
    


class AnsiCursor(object):
    def UP(self, n=...):
        ...
    
    def DOWN(self, n=...):
        ...
    
    def FORWARD(self, n=...):
        ...
    
    def BACK(self, n=...):
        ...
    
    def POS(self, x=..., y=...):
        ...
    


class AnsiFore(AnsiCodes):
    BLACK = ...
    RED = ...
    GREEN = ...
    YELLOW = ...
    BLUE = ...
    MAGENTA = ...
    CYAN = ...
    WHITE = ...
    RESET = ...
    LIGHTBLACK_EX = ...
    LIGHTRED_EX = ...
    LIGHTGREEN_EX = ...
    LIGHTYELLOW_EX = ...
    LIGHTBLUE_EX = ...
    LIGHTMAGENTA_EX = ...
    LIGHTCYAN_EX = ...
    LIGHTWHITE_EX = ...


class AnsiBack(AnsiCodes):
    BLACK = ...
    RED = ...
    GREEN = ...
    YELLOW = ...
    BLUE = ...
    MAGENTA = ...
    CYAN = ...
    WHITE = ...
    RESET = ...
    LIGHTBLACK_EX = ...
    LIGHTRED_EX = ...
    LIGHTGREEN_EX = ...
    LIGHTYELLOW_EX = ...
    LIGHTBLUE_EX = ...
    LIGHTMAGENTA_EX = ...
    LIGHTCYAN_EX = ...
    LIGHTWHITE_EX = ...


class AnsiStyle(AnsiCodes):
    BRIGHT = ...
    DIM = ...
    NORMAL = ...
    RESET_ALL = ...


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()
