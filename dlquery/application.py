"""Module containing the logic for the dlquery GUI application."""

# from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from os import path
import webbrowser
from dlquery import create_from_csv_file
from dlquery import create_from_csv_data
from dlquery import create_from_json_file
from dlquery import create_from_json_data
from dlquery import create_from_yaml_file
from dlquery import create_from_yaml_data


class Content:
    """Content class

    Attributes
    ----------
    data (str): a text.


    """
    def __init__(self, data='', filename=''):
        self.data = data
        self.filename = filename
        self.filetype = ''
        self.ready = False
        self.process()

    @property
    def is_csv(self):
        """Check if filename or content is in csv format."""
        return self.filetype == 'csv'

    @property
    def is_json(self):
        """Check if filename or content is in json format."""
        return self.filetype == 'json'

    @property
    def is_yaml(self):
        """Check if filename or content is in yaml format."""
        return self.filetype in ['yaml', 'yml']

    @property
    def is_ready(self):
        """Check if content is ready to use."""
        return self.ready

    def process(self):
        """Analyze `self.filename` or `self.data` and
        assign equivalent `self.filetype`"""
        if self.filename:
            _, ext = path.splitext(self.filename)
            ext = ext.lower()
            if ext in ['.csv', '.json', '.yml', '.yaml']:
                self.filetype = ext[1:]

            with open(self.filename, newline='') as stream:
                self.data = stream.read()
                if self.is_csv:
                    try:
                        create_from_csv_file(self.filename)
                        self.ready = True
                    except Exception as ex:
                        raise ex
                elif self.is_json:
                    try:
                        create_from_json_file(self.filename)
                        self.ready = True
                    except Exception as ex:
                        raise ex
                elif self.is_yaml:
                    try:
                        create_from_yaml_file(self.filename)
                        self.ready = True
                    except Exception as ex:
                        raise ex
        else:
            if not self.data:
                return
            try:
                create_from_csv_data(self.data)
                self.filetype = 'csv'
                self.ready = True
            except Exception as ex:     # noqa
                try:
                    create_from_json_data(self.data)
                    self.filetype = 'json'
                    self.ready = True
                except Exception as ex:         # noqa
                    try:
                        create_from_yaml_data(self.data)
                        self.filetype = 'yaml'
                        self.ready = True
                    except Exception as ex:     # noqa
                        raise ex


class Application:
    """A dlquery GUI application class.

    Attributes
    ----------
    root (tkinter.Tk): a top tkinter app.
    content (Content): a Content instance.

    Methods
    -------
    build_menu() -> None
    run() -> None
    callback_file_open() -> None
    callback_file_exit() -> None
    callback_help_getting_started() -> None
    callback_help_view_licenses() -> None
    callback_help_about() -> None
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('800x600+100+100')
        self.root.title('DLQuery Application')
        self.root.option_add('*tearOff', False)
        self.content = None

        self.build_menu()

    @property
    def is_ready(self):
        """Check if dlquery application is ready to run."""
        if isinstance(self.content, Content):
            return self.content.is_ready
        return False

    def callback_file_exit(self):
        """Callback for Menu File > Exit."""
        self.root.quit()

    def callback_file_open(self):
        """Callback for Menu File > Open."""
        filetypes = [
            ('CSV Files', '*csv'),
            ('JSON Files', '*json'),
            ('YAML Files', '*yaml'),
            ('YML Files', '*yml')
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        self.content = Content(filename=filename)

    def callback_help_getting_started(self):
        """Callback for Menu Help > Getting Started."""
        # TODO: Need to update wiki page.
        url = 'https://github.com/Geeks-Trident-LLC/dlquery/blob/develop/README.md'
        webbrowser.open_new_tab(url)

    def callback_help_view_licenses(self):
        """Callback for Menu Help > View Licenses."""
        url = 'https://github.com/Geeks-Trident-LLC/dlquery/blob/develop/LICENSE'
        webbrowser.open_new_tab(url)

    def callback_help_about(self):
        """Callback for Menu Help > About"""
        print('help about')

    def build_menu(self):
        """Build menubar for dlquery application."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file = tk.Menu(menu_bar)
        help_ = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=file, label='File')
        menu_bar.add_cascade(menu=help_, label='Help')

        file.add_command(label='Open', command=lambda: self.callback_file_open())
        file.add_separator()
        file.add_command(label='Quit', command=lambda: self.callback_file_exit())

        help_.add_command(label='Getting Started',
                          command=lambda: self.callback_help_getting_started())
        help_.add_command(label='View Licenses',
                          command=lambda: self.callback_help_view_licenses())
        help_.add_separator()
        help_.add_command(label='About', command=lambda: self.callback_help_about())

    def run(self):
        """Launch dlquery application."""
        self.root.mainloop()


def execute():
    """Launch dlquery GUI application."""
    app = Application()
    app.run()
