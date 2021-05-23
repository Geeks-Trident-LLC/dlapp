"""Module containing the logic for the parsing utility."""

import re
import logging
from functools import partial
from dlquery.predicate import Predicate


logger = logging.getLogger(__file__)


class SelectParser:
    def __init__(self, select_statement):
        self.select_statement = select_statement
        self.select_items = []
        self.predicate = None
        self.logger = logger

    def get_predicate(self, expression):
        key, op, value = [i.strip() for i in re.split(r' +', expression, maxsplit=2)]
        key = key.replace('_SPACE_', ' ').replace('_COMMA_', ',')
        op = op.lower()
        value = value.replace('_SPACE_', ' ').replace('_COMMA_', ',')

        if op == 'is':
            func = partial(Predicate.is_, key=key, custom=value)
        elif op in ['is_not', 'isnot']:
            func = partial(Predicate.isnot, key=key, custom=value)
        elif op in ['lt', 'le', 'gt', 'ge']:
            func = partial(Predicate.compare_number, key=key, op=op, other=value)
        elif op in ['eq', 'ne']:
            func = partial(Predicate.compare, key=key, op=op, other=value)
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
        if self.select_statement == '':
            return

        select, expressions = re.split(
            ' where ', self.select_statement,
            maxsplit=1, flags=re.I
        )
        select, expressions = select.strip(), expressions.strip()
        select = re.sub('^select +', '', select, flags=re.I)

        if select and select != '*':
            self.select_items = re.split('[ ,]+', select.strip(), flags=re.I)

        if expressions:
            self.predicate = self.build_predicate(expressions)
