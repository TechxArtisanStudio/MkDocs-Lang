import logging
import logging.config
import os

def setup_logging(log_dir, default_level=logging.INFO):
    """
    Setup logging configuration
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, 'mklang.log')

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': default_level,
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': log_file_path,
                'formatter': 'standard',
                'level': default_level,
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': default_level,
        },
    }

    logging.config.dictConfig(logging_config) 