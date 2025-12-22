"""
Unofficial library for creating user bots for Discord.  
Allows automating actions, managing an account, and interacting with the Discord API without using an official bot.
Author: alx0rr
"""

from .utils.objects import *
from .utils import exceptions, log, get_userId_from_token
from .utils.logger import logging

from .client import Client
from ._async import AsyncClient


def set_log_level(level: int):
	"""
	Sets the logging level.

	:param level: The new logging level (e.g., logging.DEBUG, logging.ERROR).
	"""
	log.set_level(level)

__title__ = 'udiscord'
__author__ = 'Xsarz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025 alx0rr'
__version__ = '1.4'


from requests import get
try:__newest__ = get("https://pypi.org/pypi/udiscord/json").json().get("info", {}).get("version", __version__)
except:__newest__=__version__
if __version__ != __newest__:
	log.warning(f'{__title__} made by {__author__}. Please update the library. Your version: {__version__}  A new version: {__newest__}')