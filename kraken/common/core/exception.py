import logging as lg

_logger = lg.getLogger(__name__)


class KrakenError(Exception):
    """
    Base error class.

     :param message: Error message.
     :param args: optional Message formatting arguments.
    """

    def __init__(self, message, *args):
        super(KrakenError, self).__init__(message % args if args else message)
