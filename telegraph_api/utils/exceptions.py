__all__ = ("Error", "ServerError")

class Error(Exception):
	"""Base class for exceptions"""

class ServerError(Error):
	def __init__(self, msg: str):
		"""
		Exception ServerError
		:param msg: String
		"""
		super(Error, self).__init__(msg)