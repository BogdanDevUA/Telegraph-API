from aiohttp import ClientSession, ClientTimeout
from .api import api, BaseSite
from typing import Any, Dict, Optional, Any, Union
from asyncio import AbstractEventLoop as Loop
from contextlib import contextmanager
#from urllib.parse import urlencode
from secrets import token_hex
from .utils import BaseObject
from asyncio import get_event_loop

__all__ = ("Client")

class Client(BaseObject):
	def __init__(self, 
				name: str, 
				short_name: Optional[str]=None, *, 
				author_url: str=None,
				save_data: bool=True,
				loop: Optional[Loop]=None,
				timeout: Union[ClientTimeout, int]=10,
				**conf: Dict[str, Any]
				):
		"""
		Initialise Client

		param name: `String`
		param short_name: :obj:`Optional[str]`
		param author_url: `String`
		param save_data: `Boolean`
		param loop: :obj:`Optional[AbstractEventLoop]`
		param timeout: :obj:`Union[ClientTimeout, int]`
		param conf: :obj:`Dict[str, Any]`
		"""

		# == Checking ============================================================================
		if not isinstance(name, str):
			raise TypeError(f"name must be type str, not {type(name).__name__}")

		if len(name) > 128:
			raise TypeError(f"lenght name must be 128 >, not {len(name)}")

		if short_name:
			if len(short_name) > 32:
				raise TypeError(f"lenght short_name must be 128 >, not {len(name)}")

		if not isinstance(loop, Loop):
			raise TypeError(f"loop must be type AbstractEventLoop, not  {type(loop).__name__}")

		if not isinstance(timeout, ClientTimeout):
			timeout = ClientTimeout(total=timeout)

		# =======================================================================================

		self.name = name
		self.short_name = short_name
		self.timeout = timeout

		if not loop:
			loop = get_event_loop()

		self.loop = loop
		self.session = ClientSession(
				BaseSite, 
				loop=self.loop, 
				timeout=self.timeout
		)
		print("Session created\n")
		self.conf = conf
		# Config ____^

		# == Pending requests ==============================
		data = dict(author_name=name)
		if author_url: 
			data["author_url"] = author_url

		if short_name:
			data["short_name"] = short_name

		# ==================================================
		req = self.requests(api.createAccount, data)
		data: Dict[str, str] = self.run(req)

		self.short_name = data["short_name"]
		self.author_name = data["author_name"]
		self.author_url = data["author_url"]
		self.access_token = data["access_token"]
		self.auth_url = data["auth_url"]

		if save_data:
			import dbm

			name = f"telegraph_data{self.hash}"

			self.database = dbm.open(name) # Creating datafile

	def __enter__(self, **kwargs: Dict[str, Any]) -> object:
		"""
		Contextmanager

		param **kwargs: :obj:`Dict[str, Any]`
		return: :class:`Client`
		"""
		self.__init__(**kwargs)
		return self

	def __del__(self, *_):
		"""Deleting Client"""
		del self.database
		del self

	__aenter__ = __enter__
	__aexit__ = close = __exit__ = __del__

	async def edit_account_info(self, **kwargs: Dict[str, Any]) -> dict:
		"""
		Method `edit_account_info`

		param **kwargs: :obj:`Dict[str, Any]`
		return: `Dictonary`
		"""
		data = dict(access_token=self.access_token, **kwargs)

		return await self.requests(api.editAccountInfo, data=data)
		
	async def revoke_access_token(self):
		"""Method `revoke_access_token`"""
		data = dict(access_token=self.access_token)

		data = await self.requests(api.revokeAccessToken, data=data)
		self.access_token = data["access_token"]

	def __getitem__(self, item: str) -> Any:
		"""
		Getting item from config
		
		param item: `String`
		return: :obj:`Any`
		"""
		return self.conf.get(item)