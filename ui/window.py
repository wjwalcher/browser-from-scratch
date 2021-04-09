import tkinter as tk
import tkinter.font as tkFont
from url.urlfetcher import UrlFetch
from render.htmlrender import lex

class BrowserWindow:

    def __init__(self):
        self.WIDTH, self.HEIGHT = 1000, 800
        self.HSTEP, self.VSTEP = 13, 18
        self.SCROLL_STEP = 100
        self.scroll = 0
        self.font_size = 12
        self.fetcher = UrlFetch()
        self.window = tk.Tk()
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Control-equal>", self.magnifytext)
        self.window.bind("<Control-minus>", self.minifytext)
        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        # NOTE: These two scroll wheel bindings are Linux specific
        self.window.bind("<Button-4>", self.scrollmouseup)
        self.window.bind("<Button-5>", self.scrollmousedown)
        self.window.bind("<Configure>", self.resizewindow)

        self.canvas.pack(expand=True, fill=tk.BOTH)

    def load(self, url):

        headers, body, scheme = self.fetcher.fetchUrl(url)
        self.content = lex(body, scheme)
        self.display_list = self.layout()
        self.render()

    def render(self):
        font = tkFont.Font(family="Helvetica", size=self.font_size)
        for x, y, c in self.display_list:
            if y > self.scroll + self.HEIGHT: continue
            if y + self.VSTEP < self.scroll: continue 
            self.canvas.create_text(x, y - self.scroll, text=c, font=font)

    def magnifytext(self, e):
        self.font_size += 1
        self.HSTEP += 1
        self.VSTEP += 1
        self.display_list = self.layout()
        self.invalidateandrender()

    def minifytext(self, e):
        self.font_size -= 1
        self.HSTEP -= 1
        self.VSTEP -= 1
        self.display_list = self.layout()
        self.invalidateandrender()

    def scrolldown(self, e):
        self.scroll += self.SCROLL_STEP
        self.invalidateandrender()

    def invalidateandrender(self):
        self.canvas.delete("all")
        self.render()

    def scrollup(self, e):
        if self.scroll > 0:
            self.scroll -= self.SCROLL_STEP
            self.invalidateandrender()

    def scrollmouseup(self, e):
        self.scrollup(e)

    def scrollmousedown(self, e):
        self.scrolldown(e)

    def resizewindow(self, e):
        self.WIDTH = e.width
        self.HEIGHT = e.height
        self.display_list = self.layout()
        self.invalidateandrender()

    def layout(self):
        cursor_x, cursor_y = self.HSTEP, self.VSTEP

        display_list = []
        for c in self.content:
            display_list.append((cursor_x, cursor_y, c))
            cursor_x += self.HSTEP

            if c == "\n":
                cursor_y += self.VSTEP + 10
            elif cursor_x >= self.WIDTH - self.HSTEP:
                cursor_y += self.VSTEP
                cursor_x = self.HSTEP

        return display_list
    