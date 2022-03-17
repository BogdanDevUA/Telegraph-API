from aiohttp import ClientSession, ClientTimeout
from . import api
from typing import Any, Dict, Optional, Any, Union
from asyncio import AbstractEventLoop as Loop
from contextlib import contextmanager
#from urllib.parse import urlencode
from secrets import token_hex

class Client:
	def __init__(self, 
				name: str, 
				short_name: Optional[str]=None, *, 
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
		:param save_data: Boolean
		:param loop: :obj:`Optional[AbstractEventLoop]`
		:param timeout: :obj:`Union[ClientTimeout, int]`
		:param check_token: Boolean
		:param conf: :obj:`Dict[str, Any]`
		"""
		if not isinstance(name, str):
			raise TypeError(f"name must be type str, not {type(name).__name__}")

		if not name.istitle():
			name = name.title()

		self.name = name
		self.short_name = short_name
		if not isinstance(timeout, ClientTimeout):
			timeout = ClientTimeout(total=timeout)

		self.timeout = timeout

		if not isinstance(loop, Loop):
			raise TypeError(f"loop must be type AbstractEventLoop, not  {type(loop).__name__}")

		self.hash = token_hex(5)

		self.session = ClientSession(
				api.Base, 
				loop=loop, 
				timeout=self.timeout
		)
		print("Session created")
		self.conf = conf
		"""
		Client example:

		>>> with Client("Alex", **config) as client:
		... 	poster = Poster(client)
		...		post = poster.create_post(client["post1"])
		...		print(post.text)
		...
		Im Alex
		"""

		data = {
			"name": name,
			"short_name": short_name
		}

		try:
			with self.session.get(..., data=data) as response:
				data: Dict[str, str] = response.json()

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
		except:
			pass

		print(f'Account "{self.name}" succefull created!\nWith hash {self.hash}')

		@contextmanager
		@staticmethod
		def check_token(token: str) -> bool:
			"""
			Checking token for valid
			:param token: String
			:return: Boolean
			"""
			try:
				yield
			finally:
				pass

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