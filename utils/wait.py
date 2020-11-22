# -*- coding: utf-8 -*-
import sys
import time
import logging

from selenium.common.exceptions import TimeoutException


def wait_until(fn, timeout=10, message='', poll_frequency=1, exception=None):
    """Calls the method provided with the driver as an argument until the \
    return value is not False."""
    end_time = time.time() + timeout
    while True:
        try:
            value = fn()
            if value:
                return value
        except Exception:
            pass
        if time.time() > end_time:
            break
        time.sleep(poll_frequency)
    logging.error("过了%s秒,还没有等到期望的结果" % timeout)
    if exception is None:
        if message == "":
            message = "过了%s秒,还没有等到期望的结果" % timeout
        exception = TimeoutException(message)
    else:
        exception = exception(message)
    raise (type(exception), exception, sys.exc_info()[2])
