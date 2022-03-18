__all__ = ("BaseSite", "api")
BaseSite = "https://api.telegra.ph/"

class Item(str):
    """
    Helper item
    If a value is not provided,
    it will be automatically generated based on a variable's name
    """
    def __init__(self):
        pass
    def __get__(self, *_):
        return self.name
    def __set_name__(self, _, name: str):
        self.name = name

class api:
	"""
	API Methods for Telegraph
	"""
	createAccount = Item()
	editAccountInfo = Item()
	revokeAccessToken = Item()
	getPage = Item()
	getPageList = Item()
	createPage = Item()
	editPage = Item()
	deletePage = Item()