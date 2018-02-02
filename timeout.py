import logging
import signal
class TimeoutError(Exception):
    pass

class Timeout:
    def __init__(self, logger=logging.getLogger(__name__), seconds=1, error_message='Timeout'):
        self.logger = logger
        logging.basicConfig(level=logging.DEBUG)
        self.seconds=seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        logging.critical('TimeOut error')
        raise TimeoutError()
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        logging.info('timeout close')
        signal.alarm(0)