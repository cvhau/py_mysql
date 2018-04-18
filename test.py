# -*- coding: utf-8 -*-
from py_mysql.operators import *

# print AND({'id': GT(1)}, {'id': LTE(10)}, {'firstname': 'Hau', 'lastname': 'Van'})
# print AND({'id': BETWEEN('1', 10)}, {'firstname': 'Hau', 'lastname': 'Van'})
# print AND({'id': GT(1)}, {'id': LTE(10)}, firstname='Hau', lastname='Van')
# # id>1 AND id<=10
# print AND({'id': GT(1), 'price': LTE(10)}, firstname='Hau', lastname=NOT_IN('Van', 'Cao'))
# print OR({'id': GT(1), 'price': LTE(10)}, firstname='Hau', lastname=IN('Van', 'Cao'))
# print NOT({'id': LT(14)}, username='KAA')
# print AND(NOT(Country='Germany', username='BOL'), NOT(Country='USA'))
# print OR(AND({'id': GT(1)}, {'id': LTE(10)}, firstname='Hau', lastname='Van'), {'id': NOT_IN(4, 56)})
# print OR({'CustomerID': IN(14, 3)}, {'CustomerID': IN(7, 8)})

print AND({'Country': IS(None)}, OR({'City': IS_NOT(False)}, {'City': 'München'}))
