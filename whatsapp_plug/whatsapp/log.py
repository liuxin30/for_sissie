# -*- coding: utf-8 -*-
import os
import logging
BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

log_path = BASE_PATH + "\\whatsapp_plug.log"
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=log_format)


LOG = logging.getLogger(__name__)
