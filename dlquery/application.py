"""Module containing the logic for the dlquery GUI application."""

from tkinter import *
from tkinter import ttk


class Application:
    """A dlquery GUI application class.

    Attributes
    ----------
    root (tkinter.Tk): a top tkinter app.

    Methods
    -------
    run() -> None

    """
    def __init__(self):
        self.root = Tk()
        button = ttk.Button(self.root, text='TODO: Need to implement GUI application')
        button.pack()

    def run(self):
        self.root.mainloop()
