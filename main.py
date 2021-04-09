from ui.window import BrowserWindow
import tkinter as tk

url = input("Enter the URL to fetch: ")

browser = BrowserWindow()
browser.load(str(url))
tk.mainloop()
