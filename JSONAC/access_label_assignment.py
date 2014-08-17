import utility as utility

'''
	this script is about maintaining path/label assignment tree


'''

class Node:
	def __init__(self, label=None, tag=None,path=None):
		self.label = label
		self.tag = tag
		self.path = path

	def set_label(self, label):
		self.label = label

	def set_tag (self, tag):
		self.tag = tag

	def set_path (self, path):
		self.path = path


class PathLabelTree:
	
	def __init__(self):
		self.root = None



def test():
	a_p = utility.LoadJSON("path_label_policy.json")
	print a_p.get_json()


test()
