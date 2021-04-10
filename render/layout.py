import tkinter.font
from .htmlrender import Text, Tag

class Layout:

    def __init__(self):
        self.display_list = []
        self.HSTEP, self.VSTEP = 20, 18
        self.font_size = 12
        self.font_family = "Times"

    def incFontSize(self):
        self.font_size += 1

    def decFontSize(self):
        self.font_size -= 1

    def generateLayout(self, tokens, window_width):
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        display_list = []
        weight= "normal"
        style = "roman"

        for tok in tokens:
            if isinstance(tok, Text):
                font = tkinter.font.Font(size=self.font_size, weight=weight, slant=style)
                for word in tok.text.split():
                    
                    w = font.measure(word)

                    if word == "\n":
                        cursor_y += font.metrics("linespace") * 2.0
                        cursor_x = self.HSTEP
                        continue
                    elif cursor_x + w >= window_width - self.HSTEP:
                        cursor_y += font.metrics("linespace") * 1.2
                        cursor_x = self.HSTEP

                    display_list.append((cursor_x, cursor_y, word, font))
                    cursor_x += w + font.measure(" ")

            elif tok.tag == "i":
                style = "italic"
            elif tok.tag == "/i":
                style = "roman"
            elif tok.tag == "b":
                weight = "bold"
            elif tok.tag == "/b":
                weight = "normal"
            elif tok.tag == "small":
                self.font_size -= 2
            elif tok.tag == "/small":
                self.font_size += 2
            elif tok.tag == "big":
                self.font_size += 4
            elif tok.tag == "/big":
                self.font_size -= 4
        
        return display_list
