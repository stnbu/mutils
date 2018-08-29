# -*- mode: python; coding: utf-8 -*-

import os
import sys
import time
import tempfile
import re
import requests
import datetime
import pytz
import json
import urllib
from requests.auth import HTTPBasicAuth
import logging
import logging.handlers
import lockfile
from dateutil.parser import parse as parse_dt

import daemon
import daemon.pidfile

import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def rr(scheme, netloc, url, params='', query='', fragment='', headers={}, auth=None):
    """request+response -- given a location and query, just return the (json) data.
    Handle errors appropriately.
    """

    location = '/' + location.lstrip('/')

    url = urllib.parse.urlparse(urllib.parse.urlunparse(
        (scheme, netloc, url, params, query, fragment)
    )).geturl()

    logger.debug('trying to get {}'.format(url))
    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        logger.error('when getting {}: {}'.format(url, response.reason))
        raise Exception(response.reason)
    return response.json()
