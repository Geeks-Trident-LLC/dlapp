"""Module containing the logic for the dlquery GUI application."""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from os import path
import webbrowser
from textwrap import dedent
from dlquery import create_from_csv_file
from dlquery import create_from_csv_data
from dlquery import create_from_json_file
from dlquery import create_from_json_data
from dlquery import create_from_yaml_file
from dlquery import create_from_yaml_data


__version__ = '1.0.0'
version = __version__


def get_relative_center_location(parent, width, height):
    """get relative a center location of parent window.

    Parameters
    ----------
    parent (tkinter): tkinter component instance.
    width (int): a width of a child window.
    height (int): a height of a child window..

    Returns
    -------
    tuple: x, y location.
    """
    pwh, px, py = parent.winfo_geometry().split('+')
    px, py = int(px), int(py)
    pw, ph = [int(i) for i in pwh.split('x')]

    x = int(px + (pw - width) / 2)
    y = int(py + (ph - height) / 2)
    return x, y


class Data:
    license_name = 'BSD 3-Clause License'
    license_url = 'https://github.com/Geeks-Trident-LLC/dlquery/blob/main/LICENSE'
    repo_url = 'https://github.com/Geeks-Trident-LLC/dlquery'
    # TODO: Need to update wiki page for getting_started_url instead of README.md.
    getting_started_url = 'https://github.com/Geeks-Trident-LLC/dlquery/blob/develop/README.md'
    copyright_text = 'Copyright @ 2021 Geeks Trident LLC.  All rights reserved.'

    @classmethod
    def get_license(cls):
        license_ = """
            BSD 3-Clause License

            Copyright (c) 2021, Geeks Trident LLC
            All rights reserved.

            Redistribution and use in source and binary forms, with or without
            modification, are permitted provided that the following conditions are met:

            1. Redistributions of source code must retain the above copyright notice, this
               list of conditions and the following disclaimer.

            2. Redistributions in binary form must reproduce the above copyright notice,
               this list of conditions and the following disclaimer in the documentation
               and/or other materials provided with the distribution.

            3. Neither the name of the copyright holder nor the names of its
               contributors may be used to endorse or promote products derived from
               this software without specific prior written permission.

            THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
            AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
            IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
            DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
            FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
            DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
            SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
            CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
            OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
            OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """
        license_ = dedent(license_).strip()
        return license_


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
        self._base_title = 'DLQuery GUI'
        self.root = tk.Tk()
        self.root.geometry('800x600+100+100')
        self.root.option_add('*tearOff', False)
        self.content = None

        self.set_title()
        self.build_menu()

    @property
    def is_ready(self):
        """Check if dlquery application is ready to run."""
        if isinstance(self.content, Content):
            return self.content.is_ready
        return False

    def set_title(self, node=None, title=''):
        """Set a new title for tkinter component.

        Parameters
        ----------
        node (tkinter): a tkinter component.
        title (str): a title.  Default is empty.
        """
        node = node or self.root
        btitle = self._base_title
        title = '{} - {}'.format(title, btitle) if title else btitle
        node.title(title)

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
        webbrowser.open_new_tab(Data.getting_started_url)

    def callback_help_view_licenses(self):
        """Callback for Menu Help > View Licenses."""
        webbrowser.open_new_tab(Data.license_url)

    def callback_help_about(self):
        """Callback for Menu Help > About"""
        def mouse_over(event):
            url_lbl.config(font=url_lbl.default_font + ('underline',))
            url_lbl.config(cursor='hand2')

        def mouse_out(event):
            url_lbl.config(font=url_lbl.default_font)
            url_lbl.config(cursor='arrow')

        def mouse_press(event):
            webbrowser.open_new_tab(url_lbl.link)

        about = tk.Toplevel(self.root)
        self.set_title(node=about, title='About')
        width, height = 400, 400
        x, y = get_relative_center_location(self.root, width, height)
        about.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        about.resizable(False, False)

        # company
        company_lbl = tk.Label(about, text='DLQuery GUI v{}'.format(version))
        company_lbl.place(x=10, y=10)

        # URL
        url = Data.repo_url
        tk.Label(about, text='URL:').place(x=10, y=40)
        url_lbl = tk.Label(about, text=url, fg='blue', font=('sans-serif', 10))
        url_lbl.default_font = ('sans-serif', 10)
        url_lbl.place(x=36, y=40)
        url_lbl.link = url

        url_lbl.bind('<Enter>', mouse_over)
        url_lbl.bind('<Leave>', mouse_out)
        url_lbl.bind('<Button-1>', mouse_press)

        # license textbox
        lframe = ttk.LabelFrame(
            about, height=280, width=380,
            text=Data.license_name
        )
        lframe.place(x=10, y=80)
        txtbox = tk.Text(lframe, width=45, height=14, wrap='word')
        txtbox.grid(row=0, column=0)
        scrollbar = ttk.Scrollbar(lframe, orient=tk.VERTICAL, command=txtbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        txtbox.config(yscrollcommand=scrollbar.set)
        txtbox.insert(tk.INSERT, Data.get_license())
        txtbox.config(state=tk.DISABLED)

        # footer - copyright
        footer = tk.Label(about, text=Data.copyright_text)
        footer.place(x=10, y=360)

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
