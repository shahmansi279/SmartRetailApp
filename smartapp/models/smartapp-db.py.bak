# -*- coding: utf-8 -*-

db.define_table('users',
                 Field('uemail','string', requires=IS_NOT_EMPTY()),
                 Field('password','string',requires=IS_NOT_EMPTY()),
                 Field('role','string'),
                 Field('phone','string',requires=IS_NOT_EMPTY()),
                 Field('address','string',requires=IS_NOT_EMPTY()),
                 Field('zipcode','string',requires=IS_NOT_EMPTY()))

db.define_table('sensors',
                 Field('uemail','string',requires=IS_NOT_EMPTY()),
                 Field('sensorid','string'),
                 Field('sensortype','string',requires=IS_NOT_EMPTY()),
                 Field('sensorlocn','string',requires=IS_NOT_EMPTY()),
                 Field('sensordesc','string',requires=IS_NOT_EMPTY()),
                 Field('attr1','string'),
                 Field('attr2','string'))
