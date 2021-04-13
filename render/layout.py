import tkinter.font
from .htmlelements import Text, Element

class Layout:

    def __init__(self):
        self.display_list = []
        self.line = []

        self.HSTEP, self.VSTEP = 20, 18
        self.cursor_x, self.cursor_y = self.HSTEP, self.VSTEP

        self.font_size = 12
        self.font_family = "Times"

    def incFontSize(self):
        self.font_size += 1

    def decFontSize(self):
        self.font_size -= 1

    def open(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "h1":
            self.weight = "bold"
            self.font_size += 6
            self.should_center = True
            self.flush()
        elif tag == "br":
            self.flush()
        elif tag == "big":
            self.font_size += 4

    def close(self, tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "h1":
            self.weight = "normal"
            self.font_size -= 6
            self.should_center = False
            self.flush()
        elif tag == "p":
            self.flush()
            self.cursor_y += self.VSTEP
        elif tag == "big":
            self.font_size -= 4
            
    def flush(self):
        if not self.line: return

        metrics = [font.metrics() for x, word, font, in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        max_descent = max([metric["descent"] for metric in metrics])
        baseline = self.cursor_y + 1.2 * max_ascent

        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        
        self.line = []
        self.cursor_x = self.HSTEP
        self.cursor_y = baseline + 1.2 * max_descent

    def generateLayout(self, tree, window_width):
        # Clear old display list
        self.display_list = []
        self.cursor_x, self.cursor_y = self.HSTEP, self.VSTEP

        self.weight= "normal"
        self.style = "roman"
        self.should_center = False

        if isinstance(tree, Text):
            self.text(tree.text, window_width)
        else:
            self.open(tree.tag)
            for child in tree.children:
                self.recurseHelper(child, window_width)
            self.close(tree.tag)

        self.flush()

        return self.display_list

    def recurseHelper(self, tree, window_width):
        if isinstance(tree, Text):
            self.text(tree.text, window_width)
        else:
            self.open(tree.tag)
            for child in tree.children:
                self.recurseHelper(child, window_width)
            self.close(tree.tag)
        
    def text(self, text, window_width):
        font = tkinter.font.Font(size=self.font_size, weight=self.weight, slant=self.style)

        # Calculate entire line's width
        if (self.should_center):
            line_width = sum([font.measure(word) for word in text.split()])

        for word in text.split():
            
            w = font.measure(word)

            # FIXME: This will break when the line_width exceeds window width.
            # Write a way to break words and center in this case.
            if (self.should_center):
                self.cursor_x = int(window_width/2) - int(line_width/2)
                self.should_center = False

            if self.cursor_x + w >= window_width - self.HSTEP:
                self.flush()

            self.line.append((self.cursor_x, word, font))
            self.cursor_x += w + font.measure(" ")

