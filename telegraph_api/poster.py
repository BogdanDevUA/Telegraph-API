from .client import Client
from types import Post
from .api import api
from .utils.regexp import get_entities
from .utils.exceptions import ServerError

class Poster:
	def __init__(self, client: Client):
		"""
		Initialisation poster
		:param client: :obj:`Client`
		"""
		if not isinstance(client, Client):
			raise TypeError(f"Client must be type Client, not {type(client).__name__}")

		self.client: Client = client

	async def create_post(self, title: str, text: str) -> Post:
		"""
		Method create post

		:param title: String
		:param text: String
		:return: :obj:`Post`
		"""

		if not title.istitle():
			title = title.title()

		data = {
			"access_token": self.client.token,
			"title": title,
			"author_name": self.client.name,
			"content": [],
			"return_content": "true"
		}

		for content in get_entities(text):
			data = dict(tag=content[0], children=[content[1]])
			data["content"].append(data)

		try:
			async with self.client.session.get(api.createPage, data=data) as response:
				response = response

		except Exception as e:
			raise ServerError(str(e))

		data = await response.json()
		return Post(**data["result"])

	async def edit_post(self, id: str) -> Post:
		"""
		Method edit post

		:param id: String
		:return: :obj:`Post`
		"""
		data = {
			"access_token": self.client.token
		}

		try:
			async with self.client.session.get(api.editPage, data=data) as response:
				response = response

		except Exception as e:
			raise ServerError(str(e))

		data = await response.json()
		return Post(**data["result"])