import tkinter
import tkinter.font
from url.urlfetcher import UrlFetch
from render.htmlrender import lex, grabBody, Text, Tag
from render.layout import Layout


class BrowserWindow:

    def __init__(self):
        self.WIDTH, self.HEIGHT = 1000, 800
        self.HSTEP, self.VSTEP = 20, 18
        self.SCROLL_STEP = 100
        self.scroll = 0

        self.fetcher = UrlFetch()
        self.layout = Layout()
        self.window = tkinter.Tk()
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Control-equal>", self.magnifytext)
        self.window.bind("<Control-minus>", self.minifytext)
        self.canvas = tkinter.Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT)
            
        # NOTE: These two scroll wheel bindings are Linux specific
        self.window.bind("<Button-4>", self.scrollmouseup)
        self.window.bind("<Button-5>", self.scrollmousedown)
        self.canvas.bind("<Configure>", self.resizewindow)

        self.canvas.pack(expand=True, fill=tkinter.BOTH)

    def load(self, url):

        headers, body, scheme = self.fetcher.fetchUrl(url)
        body = grabBody(body)
        self.content = lex(body)
        print("Lexing complete")
        self.display_list = self.layout.generateLayout(
            self.content, self.WIDTH)
        print("Layout complete")
        self.render()
        print("Render complete")

    def render(self):
        for x, y, c, f in self.display_list:
            if y > self.scroll + self.HEIGHT:
                continue
            if y + self.VSTEP < self.scroll:
                continue
            self.canvas.create_text(
                x, y - self.scroll, text=c, font=f, anchor='nw')

    def invalidateandrender(self):
        self.canvas.delete("all")
        self.render()

    def magnifytext(self, e):
        self.layout.incFontSize()
        self.display_list = self.layout.generateLayout(
            self.content, self.WIDTH)
        self.invalidateandrender()

    def minifytext(self, e):
        self.layout.decFontSize()
        self.display_list = self.layout.generateLayout(
            self.content, self.WIDTH)
        self.invalidateandrender()

    def scrolldown(self, e):
        self.scroll += self.SCROLL_STEP
        self.invalidateandrender()

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
        print(e.width, e.height)
        self.display_list = self.layout.generateLayout(
            self.content, self.WIDTH)
        print("RESIZE: Layout finished, re-rendering...")
        self.invalidateandrender()
        print("RESIZE: Re-rendering complete.")
