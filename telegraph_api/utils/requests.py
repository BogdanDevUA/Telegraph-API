from .exceptions import ServerError

class baseObject:
	def __init__(self):
		pass

	async def requests(self, method: api, data: dict) -> dict:
		"""
		Method requests
		:param method: :obj:`api`
		:param data: Dictonary
		"""
		try:
			async with self.session.get(method, data=data) as response:
				response = response
		except Exception as e:
			raise ServerError(str(e))

		data = await response.json()
		return data.get("result") or data

	def run(self, req: self.requests) -> dict:
		if not isinstance(req, self.requests):
			raise TypeError(f"req must be type baseObject.requests, not {type(req).__name__}")

		return self.loop.run_until_complete(requests)
		