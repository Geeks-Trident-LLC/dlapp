"""Module containing the logic for the dlquery GUI."""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from os import path
import webbrowser
from textwrap import dedent
from dlquery import create_from_csv_data
from dlquery import create_from_json_data
from dlquery import create_from_yaml_data


__version__ = '1.0.0'
version = __version__

__edition__ = 'Community Edition'
edition = __edition__


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
    repo_url = 'https://github.com/Geeks-Trident-LLC/dlquery'
    license_url = path.join(repo_url, 'blob/main/LICENSE')
    # TODO: Need to update wiki page for documentation_url instead of README.md.
    documentation_url = path.join(repo_url, 'blob/develop/README.md')
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
    def __init__(self, data='', filename='', filetype=''):
        self.data = data
        self.filename = filename
        self.filetype = filetype
        self.ready = False
        self.query_obj = None
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

    def process_filename(self):
        if self.filename:
            _, ext = path.splitext(self.filename)
            ext = ext.lower()
            if ext in ['.csv', '.json', '.yml', '.yaml']:
                ext = ext[1:]
                ext = 'yaml' if ext in ['yml', 'yaml'] else ext
                self.filetype = ext

            with open(self.filename, newline='') as stream:
                self.data = stream.read().strip()

                if not self.data:
                    msg = 'TODO: implement case file - Content.data is empty'
                    raise NotImplementedError(msg)

    def process_data(self):
        if not self.data:
            msg = 'TODO: implement case Content.data is emtpy'
            raise NotImplementedError(msg)
        if not self.filetype:
            msg = 'TODO: implement case data - Content.filetype is empty'
            raise NotImplementedError(msg)

        if self.is_yaml:
            try:
                self.query_obj = create_from_yaml_data(self.data)
                self.ready = True
            except Exception as ex:
                msg = '{}: {}'.format(type(ex), ex)
                raise NotImplementedError(msg)
        elif self.is_json:
            try:
                self.query_obj = create_from_json_data(self.data)
                self.ready = True
            except Exception as ex:
                msg = '{}: {}'.format(type(ex), ex)
                raise NotImplementedError(msg)
        elif self.is_csv:
            try:
                self.query_obj = create_from_csv_data(self.data)
                self.ready = True
            except Exception as ex:
                msg = '{}: {}'.format(type(ex), ex)
                raise NotImplementedError(msg)

    def process(self):
        """Analyze `self.filename` or `self.data` and
        assign equivalent `self.filetype`"""
        self.process_filename()
        self.process_data()


class Application:
    """A dlquery GUI class.

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
    callback_help_documentation() -> None
    callback_help_view_licenses() -> None
    callback_help_about() -> None
    """
    def __init__(self):
        self._base_title = 'DLQuery GUI'
        self.root = tk.Tk()
        self.root.geometry('800x600+100+100')
        self.root.minsize(200, 200)
        self.root.option_add('*tearOff', False)
        self.content = None

        self.panedwindow = None
        self.text_frame = None
        self.entry_frame = None
        self.result_frame = None

        self.radio_btn_var = tk.StringVar()
        self.lookup_entry_var = tk.StringVar()
        self.select_entry_var = tk.StringVar()
        self.result = None

        self.textarea = None
        self.csv_radio_btn = None
        self.json_radio_btn = None
        self.yaml_radio_btn = None

        self.set_title()
        self.build_menu()
        self.build_frame()
        self.build_textarea()
        self.build_entry()
        self.build_result()

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
            ('JSON Files', '*json'),
            ('YAML Files', '*yaml'),
            ('YML Files', '*yml'),
            ('CSV Files', '*csv')
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            content = Content(filename=filename)
            if content.is_ready:
                self.set_title(title=filename)
                self.textarea.delete("1.0", "end")
                self.textarea.insert(tk.INSERT, content.data)
                self.radio_btn_var.set(content.filetype)

    def callback_help_documentation(self):
        """Callback for Menu Help > Getting Started."""
        webbrowser.open_new_tab(Data.documentation_url)

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
        fmt = 'DLQuery GUI v{} ({})'
        company_lbl = tk.Label(about, text=fmt.format(version, edition))
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
        scrollbar.grid(row=0, column=1, sticky='nsew')
        txtbox.config(yscrollcommand=scrollbar.set)
        txtbox.insert(tk.INSERT, Data.get_license())
        txtbox.config(state=tk.DISABLED)

        # footer - copyright
        footer = tk.Label(about, text=Data.copyright_text)
        footer.place(x=10, y=360)

    def build_menu(self):
        """Build menubar for dlquery GUI."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file = tk.Menu(menu_bar)
        help_ = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=file, label='File')
        menu_bar.add_cascade(menu=help_, label='Help')

        file.add_command(label='Open', command=lambda: self.callback_file_open())
        file.add_separator()
        file.add_command(label='Quit', command=lambda: self.callback_file_exit())

        help_.add_command(label='Documentation',
                          command=lambda: self.callback_help_documentation())
        help_.add_command(label='View Licenses',
                          command=lambda: self.callback_help_view_licenses())
        help_.add_separator()
        help_.add_command(label='About', command=lambda: self.callback_help_about())

    def build_frame(self):
        """Build layout for dlquery GUI."""
        self.panedwindow = ttk.Panedwindow(self.root, orient=tk.VERTICAL)
        self.panedwindow.pack(fill=tk.BOTH, expand=True)

        self.text_frame = ttk.Frame(
            self.panedwindow, width=600, height=400, relief=tk.RIDGE
        )
        self.entry_frame = ttk.Frame(
            self.panedwindow, width=600, height=100, relief=tk.RIDGE
        )
        self.result_frame = ttk.Frame(
            self.panedwindow, width=600, height=100, relief=tk.RIDGE
        )
        self.panedwindow.add(self.text_frame, weight=7)
        self.panedwindow.add(self.entry_frame)
        self.panedwindow.add(self.result_frame, weight=2)

    def build_textarea(self):
        """Build input text for dlquery GUI."""

        self.text_frame.rowconfigure(0, weight=1)
        self.text_frame.columnconfigure(0, weight=1)
        self.textarea = tk.Text(self.text_frame, width=20, height=5, wrap='none')
        self.textarea.grid(row=0, column=0, sticky='nswe')
        vscrollbar = ttk.Scrollbar(
            self.text_frame, orient=tk.VERTICAL, command=self.textarea.yview
        )
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar = ttk.Scrollbar(
            self.text_frame, orient=tk.HORIZONTAL, command=self.textarea.xview
        )
        hscrollbar.grid(row=1, column=0, sticky='ew')
        self.textarea.config(
            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set
        )

    def build_entry(self):
        """Build input entry for dlquery GUI."""
        def callback_run_btn():
            data = self.textarea.get('1.0', 'end').strip()
            filetype = self.radio_btn_var.get()
            lookup = self.lookup_entry_var.get()
            select = self.select_entry_var.get()

            content = Content(data=data, filetype=filetype)
            if not content.is_ready:
                msg = 'TODO: show error message'
                raise NotImplementedError(msg)

            try:
                result = content.query_obj.find(lookup=lookup, select=select)
                self.result = result
                print('------------------')
                print(result)

            except Exception as ex:
                msg = 'TODO: entry-run {}: {}'.format(type(ex), ex)
                raise NotImplementedError(msg)

        def callback_clear_text_btn():
            self.textarea.delete("1.0", "end")
            self.radio_btn_var.set('')
            self.set_title()

        def callback_paste_text_btn():
            data = self.root.clipboard_get()
            if data:
                self.set_title(title='<<PASTE - Clipboard>>')
                self.textarea.delete("1.0", "end")
                self.content = Content(data=data)
                if self.content.is_ready:
                    self.textarea.insert(tk.INSERT, data)
                    self.radio_btn_var.set(self.content.filetype)
                else:
                    raise NotImplementedError('TODO: Need to show error in Result Frame')

        def callback_clear_lookup_entry():
            self.lookup_entry_var.set('')

        def callback_clear_select_entry():
            self.select_entry_var.set('')

        # run button
        run_btn = ttk.Button(self.entry_frame, text='Run',
                             command=callback_run_btn)
        run_btn.place(x=10, y=10)

        # open button
        open_file_btn = ttk.Button(self.entry_frame, text='Open',
                                   command=self.callback_file_open)
        open_file_btn.place(x=90, y=10)

        # paste button
        paste_text_btn = ttk.Button(self.entry_frame, text='Paste',
                                    command=callback_paste_text_btn)
        paste_text_btn.place(x=170, y=10)

        # clear button
        clear_text_btn = ttk.Button(self.entry_frame, text='Clear',
                                    command=callback_clear_text_btn)
        clear_text_btn.place(x=250, y=10)

        # radio buttons
        self.csv_radio_btn = ttk.Radiobutton(
            self.entry_frame, text='csv', variable=self.radio_btn_var,
            value='csv'
        )
        self.csv_radio_btn.place(x=340, y=10)

        self.json_radio_btn = ttk.Radiobutton(
            self.entry_frame, text='json', variable=self.radio_btn_var,
            value='json'
        )
        self.json_radio_btn.place(x=390, y=10)

        self.yaml_radio_btn = ttk.Radiobutton(
            self.entry_frame, text='yaml', variable=self.radio_btn_var,
            value='yaml'
        )
        self.yaml_radio_btn.place(x=450, y=10)

        # lookup entry
        lbl = ttk.Label(self.entry_frame, text='Lookup')
        lbl.place(x=10, y=40)
        lookup_entry = ttk.Entry(self.entry_frame, width=107,
                                 textvariable=self.lookup_entry_var)
        lookup_entry.place(x=60, y=40)
        lookup_entry.bind('<Return>', lambda event: callback_run_btn())

        # clear button
        clear_lookup_btn = ttk.Button(self.entry_frame, text='Clear',
                                      command=callback_clear_lookup_entry)
        clear_lookup_btn.place(x=715, y=40)

        # select statement entry
        lbl = ttk.Label(self.entry_frame, text='Select')
        lbl.place(x=10, y=68)
        select_entry = ttk.Entry(self.entry_frame, width=107,
                                 textvariable=self.select_entry_var)
        select_entry.place(x=60, y=68)
        select_entry.bind('<Return>', lambda event: callback_run_btn())

        # clear button
        clear_select_btn = ttk.Button(self.entry_frame, text='Clear',
                                      command=callback_clear_select_entry)
        clear_select_btn.place(x=715, y=68)

    def build_result(self):
        """Build result text"""

    def run(self):
        """Launch dlquery GUI."""
        self.root.mainloop()


def execute():
    """Launch dlquery GUI."""
    app = Application()
    app.run()
