"""Module containing the logic for the parsing utility."""

import re
import logging
from functools import partial
from dlquery.predicate import Predicate
from dlquery.utils import is_number


logger = logging.getLogger(__file__)


class SelectParser:
    """A Select Parser class.

    Attributes
    ----------
    select_statement (str): a select-statement.
    columns (list): columns
    predicate (function): a callable function.
    logger (logging.Logger): a logger

    Properties
    ----------
    is_zero_select -> bool
    is_all_select -> bool

    Methods
    -------
    get_predicate(expression) -> function
    build_predicate() -> function
    parse_statement() -> None
    """
    def __init__(self, select_statement):
        self.select_statement = select_statement
        self.columns = [None]
        self.predicate = None
        self.logger = logger

    @property
    def is_zero_select(self):
        """Return True if no column is selected."""
        return self.columns == [None]

    @property
    def is_all_select(self):
        """Return True if all columns are selected"""
        return self.columns == []

    def get_predicate(self, expression):
        """Parse an expression and convert to callable predicate function.

        Parameters
        ----------
        expression (str): an expression.  It can be a left express or a right expression.

        Returns
        -------
        function: a callable function.
        """
        key, op, value = [i.strip() for i in re.split(r' +', expression, maxsplit=2)]
        key = key.replace('_SPACE_', ' ').replace('_COMMA_', ',')
        op = op.lower()
        value = value.replace('_SPACE_', ' ').replace('_COMMA_', ',')

        if op == 'is':
            func = partial(Predicate.is_, key=key, custom=value)
        elif op in ['is_not', 'isnot']:
            func = partial(Predicate.isnot, key=key, custom=value)
        elif op in ['lt', 'le', 'gt', 'ge']:
            val = str(value).strip()
            pattern = r'''
                (?i)((?P<semantic>semantic)_)?
                version[(](?P<expected_version>.+)[)]$
            '''
            match_version = re.match(pattern, val, flags=re.VERBOSE)

            pattern = r'''
                (?i)(?P<name>datetime|date|time)[(]
                (?P<datetime_str>.+)
                [)]$
            '''
            match_datetime = re.match(pattern, val, flags=re.VERBOSE)

            if match_version:
                semantic = match_version.group('semantic')
                expected_version = match_version.group('expected_version')
                if not semantic:
                    func = partial(Predicate.compare_version, key=key,
                                   op=op, other=expected_version)
                else:
                    func = partial(Predicate.compare_semantic_version,
                                   key=key, op=op, other=expected_version)
            elif match_datetime:
                name = match_datetime.group('name').lower()
                datetime_str = match_datetime.group('datetime_str')
                if name == 'date':
                    func = partial(Predicate.compare_date, key=key,
                                   op=op, other=datetime_str)
            else:
                func = partial(Predicate.compare_number, key=key,
                               op=op, other=value)
        elif op in ['eq', 'ne']:
            val = str(value).strip()
            pattern = r'''
                (?i)((?P<semantic>semantic)_)?
                version[(](?P<expected_version>.+)[)]$
            '''
            match_version = re.match(pattern, val, flags=re.VERBOSE)

            pattern = r'''
                (?i)(?P<name>datetime|date|time)[(]
                (?P<datetime_str>.+)
                [)]$
            '''
            match_datetime = re.match(pattern, val, flags=re.VERBOSE)

            if match_version:
                semantic = match_version.group('semantic')
                expected_version = match_version.group('expected_version')
                if not semantic:
                    func = partial(Predicate.compare_version, key=key,
                                   op=op, other=expected_version)
                else:
                    func = partial(Predicate.compare_semantic_version,
                                   key=key, op=op, other=expected_version)
            elif match_datetime:
                name = match_datetime.group('name').lower()
                datetime_str = match_datetime.group('datetime_str')
                if name == 'date':
                    func = partial(Predicate.compare_date, key=key,
                                   op=op, other=datetime_str)
            else:
                cfunc = Predicate.compare_number if is_number(value) else Predicate.compare
                func = partial(cfunc, key=key, op=op, other=value)
        elif op == 'match':
            func = partial(Predicate.match, key=key, pattern=value)
        elif op in ['not_match', 'notmatch']:
            func = partial(Predicate.notmatch, key=key, pattern=value)
        elif op in ['contain', 'contains']:
            func = partial(Predicate.contain, key=key, other=value)
        elif re.match('not_?contains?', op, re.I):
            func = partial(Predicate.notcontain, key=key, other=value)
        elif op in ['belong', 'belongs']:
            func = partial(Predicate.belong, key=key, other=value)
        elif re.match('not_?belongs?', op, re.I):
            func = partial(Predicate.notbelong, key=key, other=value)
        else:
            msg = (
                '*** Return False because of an unsupported {!r} logical '
                'operator.  Contact developer to support this case.'
            ).format(op)
            self.logger.info(msg)
            func = partial(Predicate.false)
        return func

    def build_predicate(self, expressions):
        """Build a predicate by parsing expressions

        Parameters
        ----------
        expressions (str): single or multiple expressions.

        Returns
        -------
        function: a callable function.
        """
        def chain(data_, a_=None, b_=None, op_=''):
            result_a, result_b = a_(data_), b_(data_)
            if op_ == 'or_':
                return result_a or result_b
            elif op_ == 'and_':
                return result_a and result_b
            else:
                msg_ = (
                    '* Return False because of an unsupported {!r} logical '
                    'operator.  Contact developer to support this case.'
                ).format(op_)
                self.logger.info(msg_)
                return Predicate.false(data_)

        groups = []
        start = 0
        for match in re.finditer(' +(or_|and_) +', expressions, flags=re.I):
            expr = match.string[start:match.start()]
            op = match.group().strip().lower()
            groups.extend([expr.strip(), op.strip()])
            start = match.end()
        else:
            if groups:
                expr = match.string[match.end():].strip()
                groups.append(expr)

        if groups:
            total = len(groups)
            if total % 2 == 1 and total > 2:
                result = self.get_predicate(groups[0])
                for case, expr in zip(groups[1:-1:2], groups[2::2]):
                    func_b = self.get_predicate(expr)
                    result = partial(chain, a_=result, b_=func_b, op_=case)
                return result
            else:
                msg = (
                    '* Return False because of an invalid {!r} '
                    'expression.  Contact developer for this case.'
                ).format(expressions)
                self.logger.info(msg)
                result = partial(Predicate.false)
                return result
        else:
            return self.get_predicate(expressions)

    def parse_statement(self):
        """Parse, analyze, and build a select-statement to selecting
        columns and a callable predicate"""
        statement = self.select_statement

        if statement == '':
            return

        if ' where ' in statement.lower():
            select, expressions = re.split(
                ' +where +', statement, maxsplit=1, flags=re.I
            )
            select, expressions = select.strip(), expressions.strip()
            select = re.sub('^select +', '', select, flags=re.I)
        elif self.select_statement.lower().startswith('where'):
            select = None
            expressions = re.sub('^where +', '', statement, flags=re.I)
        else:
            select = re.sub('^select +', '', statement, flags=re.I)
            expressions = None

        if select:
            if select in ['*', '__ALL__']:
                self.columns = []
            else:
                self.columns = re.split('[ ,]+', select.strip(), flags=re.I)

        if expressions:
            self.predicate = self.build_predicate(expressions)
