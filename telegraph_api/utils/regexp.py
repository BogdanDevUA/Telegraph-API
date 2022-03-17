import html
import re
from re import MULTILINE
from typing import List, Tuple

pattern = re.compile(r"<(?P<tag>(?:b|i|s|code|u))>([^<]+)</(?P=tag)>", MULTILINE)

def get_entities(text: str) -> List[Tuple[str]]:
	"""
	Getting entities from text
	:param text: String
	:return: :obj:`List[Tuple[str]]`
	"""
	text = html.escape(text)
	return re.findall(pattern, text)