# -*- mode: python; coding: utf-8 -*-

import urllib
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_json(url, headers={}, auth=None):
    """request+response -- url, just return the (json) data.
    Handle errors appropriately.
    """

    if not isinstance(url, str):
        url = url.geturl()

    logger.debug('trying to get {}'.format(url))
    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        logger.error('when getting {}: {}'.format(url, response.reason))
        raise Exception(response.reason)
    return response.json()
