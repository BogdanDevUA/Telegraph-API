from .client import Client
from types import Post
from .api import api
from .utils.regexp import get_entities
from .utils import BaseObject


def add_content(text: str, data: dict):
	for content in get_entities(text):
		data_ = dict(tag=content[0], children=[content[1]])
		data["content"].append(data_)


class Poster(BaseObject):
	def __init__(self, client: Client):
		"""
		Initialisation poster
		:param client: :obj:`Client`
		"""
		if not isinstance(client, Client):
			raise TypeError(f"Client must be type Client, not {type(client).__name__}")

		self.client: Client = client
		self.session = self.client.session

	async def create_post(self, title: str, text: str) -> Post:
		"""
		Method create post

		:param title: String
		:param text: String
		:return: :obj:`Post`
		"""

		data = {
			"access_token": self.client.access_token,
			"title": title.title(),
			"author_name": self.client.name,
			"content": [],
			"return_content": "true"
		}

		add_content(text, data)

		data = await self.requests(api.createPage, data)
		return Post(**data)

	async def edit_post(self, patch: str, *, title: str, text: str) -> Post:
		"""
		Method edit post

		:param id: String
		:return: :obj:`Post`
		"""
		data = {
			"access_token": self.client.access_token,
			"author_url": self.author_url,
			"author_name": self.author_name,
			"patch": patch,
			"title": title,
			"content": [],
			"return_content": "true"
		}

		add_content(text, data)

		data = await self.requests(api.editPage, data)
		return Post(**data)

	async def get_page(self, patch: str) -> Post:
		"""
		Method get_page
		:param patch: URL
		:return: :obj:`Post`
		"""
		data = {
			"patch": patch,
			"return_content": "true"
		}

		data = await self.requests(api.getPage, data)
		return Post(**data)

	async def get_page_list(self, offset: int=0, limit: int=50):
		data = {
			"access_token": self.client.access_token,
			"offset": offset,
			"limit": limit
		}

		data = await self.requests(api.getPageList, data)
		return Post(**data)