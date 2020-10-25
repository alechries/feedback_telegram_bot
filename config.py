import logging.config

# CONNECTION
TELEGRAM_TOKEN = '1302818156:AAFXShtjCrESs5j4HrsbXnRJgNRdvOTnN7w'
DATABASE_PATH = 'chat.db'

# USERS ID
FEEDBACK_USER_ID = 389361183

# LOGGING TEMPLATE
logging.config.dictConfig({
    'disable_existing_loggers': True,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
})
