from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Post:
	"""
	Type Post
	:param text: String
	:param id: String
	:param url: String
	:param entities: :obj:`Dict[str, Any]`
	"""
	text: str
	id: str
	url: str
	entities: Dict[str, Any]