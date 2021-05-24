"""Module containing the logic for utilities."""


class Printer:
    @classmethod
    def print(cls, data, header='', footer='', failure_msg='', print_func=None):
        headers = str(header).splitlines()
        footers = str(footer).splitlines()
        data = data if isinstance(data, (list, tuple)) else [data]
        lst = []
        for item in data:
            lst.extend(str(item).splitlines())
        width = max(len(str(i)) for i in lst + headers + footers)
        print_func = print if print_func is None else print_func
        print_func('+-{}-+'.format('-' * width))
        if header:
            for item in headers:
                print_func('| {} |'.format(item.ljust(width)))
            print_func('+-{}-+'.format('-' * width))

        for item in lst:
            print_func('| {} |'.format(item.ljust(width)))
        print_func('+-{}-+'.format('-' * width))

        if footer:
            for item in footers:
                print_func('| {} |'.format(item.ljust(width)))
            print_func('+-{}-+'.format('-' * width))

        if failure_msg:
            print_func(failure_msg)

    @classmethod
    def print_tabular(cls, data):
        pass
