# -*- coding: utf-8 -*-
# MySQL Where Operators
import datetime


class Operator(object):
    def __init__(self):
        pass

    def compile(self):
        raise NotImplementedError("Method '%s' must be implemented" % self.compile.__name__)

    def validate(self, value):
        if isinstance(value, basestring):
            value = "'{0}'".format(value)
        elif isinstance(value, datetime.datetime):
            value = "'{0}'".format(value.strftime('%Y-%m-%d %H:%M:%S'))
        elif isinstance(value, datetime.date):
            value = "'{0}'".format(value.strftime('%Y-%m-%d'))
        elif isinstance(value, datetime.time):
            value = "'{0}'".format(value.strftime('%H:%M:%S'))
        elif value is None:
            value = "{0}".format('NULL')
        elif isinstance(value, bool):
            value = "{0}".format(str(value).upper())
        return value

    def validates(self, values):
        _values = []
        for v in values:
            _values.append(self.validate(v))
        return _values

    def __str__(self):
        return self.compile()


class E(Operator):
    def __init__(self, value):
        super(E, self).__init__()
        self.value = value

    def compile(self):
        return "={0}".format(self.validate(self.value))


class NE(Operator):
    def __init__(self, value):
        super(NE, self).__init__()
        self.value = value

    def compile(self):
        return "!={0}".format(self.validate(self.value))


class GT(Operator):
    def __init__(self, value):
        super(GT, self).__init__()
        self.value = value

    def compile(self):
        return ">{0}".format(self.validate(self.value))


class LT(Operator):
    def __init__(self, value):
        super(LT, self).__init__()
        self.value = value

    def compile(self):
        return "<{0}".format(self.validate(self.value))


class GTE(Operator):
    def __init__(self, value):
        super(GTE, self).__init__()
        self.value = value

    def compile(self):
        return ">={0}".format(self.validate(self.value))


class LTE(Operator):
    def __init__(self, value):
        super(LTE, self).__init__()
        self.value = value

    def compile(self):
        return "<={0}".format(self.validate(self.value))


class BETWEEN(Operator):
    def __init__(self, value1, value2):
        super(BETWEEN, self).__init__()
        self.operator = 'BETWEEN'
        self.value1 = value1
        self.value2 = value2

    def compile(self):
        return " {0} {1} AND {2}".format(self.operator, self.validate(self.value1), self.validate(self.value2))


class NOT_BETWEEN(BETWEEN):
    def __init__(self, value1, value2):
        super(NOT_BETWEEN, self).__init__(value1, value2)
        self.operator = 'NOT BETWEEN'


class LIKE(Operator):
    def __init__(self, pattern):
        super(LIKE, self).__init__()
        self.pattern = str(pattern)
        self.operator = 'LIKE'

    def compile(self):
        return " {0} {1}".format(self.operator, self.validate(self.pattern))


class NOT_LIKE(LIKE):
    def __init__(self, pattern):
        super(NOT_LIKE, self).__init__(pattern)
        self.operator = 'NOT LIKE'


class IN(Operator):                    # Missing IN (SELECT STATEMENT);
    def __init__(self, *args):
        super(IN, self).__init__()
        self.values = args
        self.operator = 'IN'

    def compile(self):
        num_values = len(self.values)
        q = []
        for i in xrange(num_values):
            q.append('{%s}' % i)
        q = ','.join(q)
        return " {0}({1})".format(self.operator, q).format(*self.validates(self.values))


class NOT_IN(IN):
    def __init__(self, *args):
        super(NOT_IN, self).__init__(*args)
        self.operator = 'NOT IN'


class AND(Operator):
    def __init__(self, *args, **kwargs):
        super(AND, self).__init__()
        self.operator = 'AND'
        self.args = args
        self.kwargs = kwargs

    def compile(self):
        q = []
        for arg in self.args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    if isinstance(v, Operator):
                        q.append("{0}{1}".format(k, self.validate(v)))
                    else:
                        q.append("{0}={1}".format(k, self.validate(v)))
            else:
                q.append("{0}".format(self.validate(arg)))
        for k, v in self.kwargs.iteritems():
            if isinstance(v, Operator):
                q.append("{0}{1}".format(k, self.validate(v)))
            else:
                q.append("{0}={1}".format(k, self.validate(v)))
        q = "({0})".format(" {0} ".format(self.operator).join(q))
        return q


class OR(AND):
    def __init__(self, *args, **kwargs):
        super(OR, self).__init__(*args, **kwargs)
        self.operator = 'OR'


class NOT(Operator):
    def __init__(self, *args, **kwargs):
        super(NOT, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def compile(self):
        q = []
        for arg in self.args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    if isinstance(v, Operator):
                        q.append("{0}{1}".format(k, self.validate(v)))
                    else:
                        q.append("{0}={1}".format(k, self.validate(v)))
            else:
                q.append("{0}".format(self.validate(arg)))
        for k, v in self.kwargs.iteritems():
            if isinstance(v, Operator):
                q.append("{0}{1}".format(k, self.validate(v)))
            else:
                q.append("{0}={1}".format(k, self.validate(v)))
        q = "NOT({0})".format(" AND ".join(q))
        return q


class IS(Operator):
    def __init__(self, value):
        super(IS, self).__init__()
        self.value = value
        self.operator = 'IS'

    def compile(self):
        return " {0} {1}".format(self.operator, self.validate(self.value))


class IS_NOT(IS):
    def __init__(self, value):
        super(IS_NOT, self).__init__(value)
        self.operator = 'IS NOT'
