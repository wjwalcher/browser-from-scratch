import tkinter
import tkinter.font
from render.htmlparser import HTMLParser
from render.layout import Layout
from url.urlfetcher import UrlFetch


class BrowserWindow:

    def __init__(self):
        self.WIDTH, self.HEIGHT = 1000, 800
        self.HSTEP, self.VSTEP = 20, 18
        self.SCROLL_STEP = 100
        self.scroll = 0

        self.fetcher = UrlFetch()
        self.html_parser = HTMLParser()
        self.layout = Layout()
        self.window = tkinter.Tk()

        self.canvas = tkinter.Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT)

        self.initializeKeyBindings()

        self.canvas.pack(expand=True, fill=tkinter.BOTH)

    def initializeKeyBindings(self):
        self.window.bind("<Down>", self.scrollDown)
        self.window.bind("<Up>", self.scrollUp)
        self.window.bind("<Control-equal>", self.magnifyText)
        self.window.bind("<Control-minus>", self.minifyText)
        # NOTE: These two scroll wheel bindings are Linux specific
        self.window.bind("<Button-4>", self.scrollMouseUp)
        self.window.bind("<Button-5>", self.scrollMouseDown)
        self.canvas.bind("<Configure>", self.resizeWindow)

    def load(self, url):
        headers, body, scheme = self.fetcher.fetchUrl(url)
        self.root = self.html_parser.parse(body)
        self.display_list = self.layout.generateLayout(self.root, self.WIDTH)
        self.render()

    def render(self):
        for x, y, c, f in self.display_list:
            if y > self.scroll + self.HEIGHT:
                continue
            if y + self.VSTEP < self.scroll:
                continue

            self.canvas.create_text(
                x, y - self.scroll, text=c, font=f, anchor='nw')

    def invalidateAndRerender(self):
        self.canvas.delete("all")
        self.render()

    def magnifyText(self, e):
        self.layout.incFontSize()
        self.display_list = self.layout.generateLayout(
            self.page_elements, self.WIDTH)
        self.invalidateAndRerender()

    def minifyText(self, e):
        self.layout.decFontSize()
        self.display_list = self.layout.generateLayout(
            self.page_elements, self.WIDTH)
        self.invalidateAndRerender()

    def scrollDown(self, e):
        self.scroll += self.SCROLL_STEP
        self.invalidateAndRerender()

    def scrollUp(self, e):
        if self.scroll > 0:
            self.scroll -= self.SCROLL_STEP
            self.invalidateAndRerender()

    def scrollMouseUp(self, e):
        self.scrollUp(e)

    def scrollMouseDown(self, e):
        self.scrollDown(e)

    def resizeWindow(self, e):
        self.WIDTH = e.width
        self.HEIGHT = e.height

        self.display_list = self.layout.generateLayout(
            self.root, self.WIDTH)

        self.invalidateAndRerender()
