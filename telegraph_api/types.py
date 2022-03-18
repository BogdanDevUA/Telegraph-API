from typing import Union, Dict

__all__ = ("Post")

Any = Union[str, int, list, dict]

class Data:
	def __init__(self, **kwargs: Dict[str, Any]):
		for key in kwargs:
			setattr(self, key, kwargs[key])

class Post(Data):
	"""
	Type Post
	:param text: String
	:param id: String
	:param url: String
	:param entities: :obj:`Dict[str, Any]`
	"""