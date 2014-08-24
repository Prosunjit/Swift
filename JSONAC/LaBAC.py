import sys
class Label(object):
	
	def __init__(self,name):
		self.name = name
		# for object label we need all labels that are junior to a given label
		self.junior_labels = []
		self.senior_labels = []
	
	@property
        def is_senior_to(self):
                return self.junior_labels

	# return set of direct junior roles
	@is_senior_to.setter	
	def is_senior_to(self,label):
		self.junior_labels.append(label)
	

	@property
	def is_junior_to(self):
		return self.senior_labels

	@is_junior_to.setter
	def is_junior_to(self,label):
		self.senior_labels.append(label)

	# find all junior labels to this label
	def all_junior_labels(self):
		juniors =  self._all_junior_labels()
		if self in juniors:
			juniors.remove(self)
		return juniors
	
	def _all_junior_labels(self):
		res = []
		for l in iter(self.is_senior_to):
			res += l._all_junior_labels()
		# assuming a node is junior to itself
		return res + [self]

	def all_senior_labels(self):
		seniors = self._all_senior_labels()
		if self in seniors:
			seniors.remove(self)
		return seniors
		
	def _all_senior_labels(self):
		res = []
		for s in iter(self.is_junior_to):
			res += s._all_senior_labels()
		return res + [self]


'''
        Object label class. All the junior label of a label is maintained with 
	a label.
'''
class ObjectLabel(Label, object):
	
	def __init__(self, name):
		Label.__init__(self,name)
		#self.name = name
		# cleared_label  means the user label that have access this object label  as specified in the policy.
		self.cleared_u_label = []
		# inferred_label means inferred user labels that have access to this object label by user label hierarchy
		self.inferred_u_label = []


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

class UserLabel(Label,object):
	def __init__(self, name):
		Label.__init__(self,name)
		# senior labels are all the labels that are senior from this label




		


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
		yy.is_junior_to = xx
		
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
	
	def get_junior_labels(self):
		res = {}
		for label in iter(self.labels):
			#t =  (label, label.all_junior_labels())
			res[label] = label.all_junior_labels()
			#res.append(t)
		return res
	def get_senior_labels(self):
		res = {}
		for label in iter(self.labels):
			res[label] = label.all_senior_labels()
		return res

	def print_hierarchy(self,res):
		for k in res.keys():
			sys.stdout.write(format(k.name)+":")
			for v in res[k]:
				sys.stdout.write( v.name + " ")
			sys.stdout.write("\n")

	def get_hierarchy(self):
		print "Junior Lists"
		self.print_hierarchy( self.get_junior_labels())
		print "senior lists"
		self.print_hierarchy(self.get_senior_labels())

			
def test_user_label_hierarchy():
	ulh = LabelHierarchy(user=True)
	ulh.add_x_dominates_y(x="u1",y="u2")
	ulh.add_x_dominates_y(x="u2",y="u3")
	print ulh.get_hierarchy()

#status= working
def test_object_hierarchy():
	olh = LabelHierarchy()
	olh.add_x_dominates_y(x="o1",y="o2")
	olh.add_x_dominates_y(x="o2",y="o3")
	print olh.get_hierarchy()

#status = working
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
	test_user_label_hierarchy()
