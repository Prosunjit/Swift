'''
        Object label class. All the junior label of a label is maintained with 
	a label.
'''
class ObjectLabel(object):
	
	def __init__(self, name):
		self.name = name
		# cleared_label  means the user label that have access this object label  as specified in the policy.
		self.cleared_u_label = []
		# inferred_label means inferred user labels that have access to this object label by user label hierarchy
		self.inferred_u_label = []
		# for object label we need all labels that are junior to a given label
		self.junior_labels = []	

	
	@property
        def is_senior_to(self):
                return self.junior_labels

	# return set of direct junior roles
	@is_senior_to.setter	
	def is_senior_to(self,label):
		self.junior_labels.append(label)
		
	# find all junior labels to this label
	def all_junior_labels(self):
		juniors =  self._all_junior_labels()
		if self.name in juniors:
			juniors.remove(self.name)
		return juniors
	
	def _all_junior_labels(self):
		res = []
		for l in iter(self.is_senior_to):
			res += l._all_junior_labels()
		# assuming a node is junior to itself
		return res + [self.name]
		

	@property
	def acl(self):
		return  self.cleared_u_label + self.inferred_u_label
		

	@property
	def cleared_user_label(self):
		return self.cleared_u_label
	
	@cleared_user_label.setter
	def cleared_user_label(self, user_label):		
		self.cleared_u_label.append(user_label)
		'''  	we need to set inferred user label, inferred_user_label of a object, 
			contains all such labels ul st ul is senior to given user_label
			
			Here I assume that user_label has already been set up for hierarchy.
		'''


	def inferred_user_label(self):
		pass
	
'''
	Class UserLabel correspond to a user label in the A/C model.
	for a user_label, our model is interested on all its senior_labels. 
	Note that user ObjectLabel class we were interested on junior_labels.
	This change in the requirement makes this code bit complicated.

'''

class UserLabel(object):
	def __init__(self, name):
		# senior labels are all the labels that are senior from this label
		self.senior_labels = []
		self.junior_lables = []
		self.name = name
	@property
	def is_junior_to(self):
		print "Following list is infact is *is_junior_to* list"
		return self.senior_labels

	@is_junior_to.setter
	def is_junior_to(self,label):
		self.senior_labels.append(label)
	
	# is_senior_to returns all the nodes that are junior to it.
	@property
	def is_senior_to(self):
		return self.junior_list

	@is_senior_to.setter
	def is_senior_to(self,label):
		try:
			self.junior_labels.append(label)
			label.is_junior_to = self
		except Exception as e:
			print e
			pass


'''
	access label hierarchy. This is essentially a partial order.

'''

class LabelHierarchy:
	def __init__(self, user=False):
		# all the root of the partial order set is stored in root_list
		self.root_list = []
		# all labels of the Label Hierarchy
		self.labels=[]
		# if object_type = True , it means it is Object_label hieararchy. otherwise userlabel hierarchy
		self.object_type = True
		if user == True:
			self.object_type = False

	def _default_hierarchy_setup(self):

		self.add_x_dominates_y(x="private",y="public")
		self.add_x_dominates_y(x="protected",y="private")

	def add_x_dominates_y(self, x=None, y=None): # insert a hierarchy of two labels such that x dominates y. x_v, y_v are values of x & y
		if self._find_node(x) == None:
			self._add_2_nodes(x)
		if self._find_node(y) == None:
			self._add_2_nodes(y)

		xx = self._find_node(x)
		yy = self._find_node(y)
		#self._add_x_dominates_y(x=xx, y=yy)
		xx.is_senior_to = yy
		
	def _add_x_dominates_y(x=None, y=None):
		#if self.object_type == True:
		x.is_senior_to = y


	def _add_2_nodes(self,x_v):
		if self.object_type == True:
			tn = ObjectLabel(x_v)
		else:
			tn = UserLabel(x_v)
		self.labels.append(tn)
		
	
	def _find_node(self,x_v):
		
		for n in self.labels:
			if n.name == x_v:
				return n
		return None
	
	def get_hierarchy(self):
		res = []
		for label in iter(self.labels):
			t =  (label.name, label.all_junior_labels())
			res.append(t)
		return res
			

def test_object_hierarchy():
	olh = LabelHierarchy()
	olh.add_x_dominates_y(x="o1",y="o2")
	olh.add_x_dominates_y(x="o2",y="o3")
	print olh.get_hierarchy()

def test_object_label():
	ol = ObjectLabel("o3")
	ol.is_senior_to = "o2"
	ol.is_senior_to = "o1"
	print ol.is_senior_to
	ol.cleared_user_label="u1"
	print ol.cleared_user_label
	print ol.acl

def test_label():
	l = Label('o1')
	l.is_senior_to = 'u1'
	l.is_senior_to = 'u2'
	print l.is_senior_to

def test():
	test_object_label()

if __name__ == "__main__":
	test_object_hierarchy()
