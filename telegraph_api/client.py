from aiohttp import ClientSession, ClientTimeout
from .api import api, BaseSite
from typing import Any, Dict, Optional, Any, Union
from asyncio import AbstractEventLoop as Loop
from contextlib import contextmanager
#from urllib.parse import urlencode
from secrets import token_hex
from .utils import baseObject
import asyncio

class Client(baseObject):
	def __init__(self, 
				name: str, 
				short_name: Optional[str]=None, *, 
				author_url: str=None,
				save_data: bool=True,
				loop: Optional[Loop]=None,
				timeout: Union[ClientTimeout, int]=10,
				check_token: bool=True,
				**conf: Dict[str, Any]
				):
		"""
		Initialise Client
		:param name: String
		:param short_name: :obj:`Optional[str]`
		:param author_url: String
		:param save_data: Boolean
		:param loop: :obj:`Optional[AbstractEventLoop]`
		:param timeout: :obj:`Union[ClientTimeout, int]`
		:param check_token: Boolean
		:param conf: :obj:`Dict[str, Any]`
		"""
		if not isinstance(name, str):
			raise TypeError(f"name must be type str, not {type(name).__name__}")

		if not isinstance(loop, Loop):
			raise TypeError(f"loop must be type AbstractEventLoop, not  {type(loop).__name__}")

		if not isinstance(timeout, ClientTimeout):
			timeout = ClientTimeout(total=timeout)

		self.name = name
		self.short_name = short_name

		self.timeout = timeout
		self.hash = token_hex(5)

		if not loop:
			loop = asyncio.get_event_loop()

		self.loop = loop
		self.session = ClientSession(
				BaseSite, 
				loop=self.loop, 
				timeout=self.timeout
		)
		print("Session created\n")
		self.conf = conf
		"""
		Client example:

		>>> with Client("Alex") as client:
		... 	poster = Poster(client)
		...		post = poster.create_post(client["post1"])
		...		print(post.text)
		...
		Session created

		Account "Alex" succefull created!
		With hash

		Im Alex
		"""

		data = dict(author_name=name)
		if author_url: 
			data["author_url"] = author_url

		if short_name:
			data["short_name"] = short_name

		data: Dict[str, str] = self.run(self.requests(api.createAccount, data=data))

		self.short_name = data["short_name"]
		self.author_name = data["author_name"]
		self.author_url = data["author_url"]
		self.access_token = data["access_token"]
		self.auth_url = data["auth_url"]

		if save_data:
			import dbm

			name = f"telegraph_data{self.hash}"

			self.database = dbm.open(name) # Creating datafile
			self.database = data

		print(f'Account "{self.name}" succefull created!\nWith hash {self.hash}\n')

	__aenter__ = __enter__ = __init__
	__aexit__ = __exit__ = __del__

	@contextmanager
	@staticmethod
	async def check_token(token: str) -> bool:
		"""
		Checking token for valid
		:param token: String
		:return: Boolean
		"""
		try:
			yield
		finally:
			pass

	async def edit_account_info(self, **kwargs: Dict[str, Any]) -> dict:
		data = dict(access_token=self.access_token, **kwargs)

		data = await self.requests(api.editAccountInfo, data=data)
		return data
		
	async def revoke_access_token(self):
		data = {"access_token": self.access_token}

		data = await self.requests(api.revokeAccessToken, data=data)
		return data

	def __del__(self):
		"""Deleting Client"""
		del self.database
		del self

	def __getitem__(self, item: str) -> Any:
		"""
		Getting item from config
		:param item: String
		:return: :obj:`Any`
		"""
		return self.conf.get(item)

	def __hash__(self) -> str:
		"""
		:return: String
		"""
		return self.hash

	__int__ = __hash__

	def __repr__(self) -> str:
		"""
		:return: String
		"""
		return f"<Client {repr(self.hash)}>"

	__str__ = __repr__