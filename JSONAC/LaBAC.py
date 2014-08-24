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
		self._cleared_u_label = []
		# inferred_label means inferred user labels that have access to this object label by user label hierarchy
		self._inferred_u_label = []

	@property
	def acl(self):
		return  self._cleared_u_label + self._inferred_u_label
		

	@property
	def cleared_user_label(self):
		return self._cleared_u_label
	
	'''
		param user_label : <Userlabel instance>
	'''
	@cleared_user_label.setter
	def cleared_user_label(self, user_label):		
		#self._cleared_u_label.append(user_label)
		self._cleared_u_label += [user_label] if user_label not in self._cleared_u_label else []
	
	'''  	we need to set inferred user label, inferred_user_label of a object, 
		contains all such labels ul st ul is senior to given user_label		
		Here I assume that user_label has already been set up for hierarchy.
	'''

	@property
	def inferred_user_label(self):
		return self._inferred_u_label

	'''
		param labels : [<UserLabel instance>, ... ]	
	'''

	@inferred_user_label.setter
	def inferred_user_label(self,labels):
		self._inferred_u_label += [l for l in labels if l not in self._inferred_u_label]
	
	def propagate(self):
		self.propagate_inferred_label(self.acl)
	
	'''
		if o1 dominates (>) o2, and o2 > o3 and so on, it method takes o1's acl 
		(both cleared & inferred label) and tie it with o2's inferred_u_label, 
		similarly, this happens for o2 and o3.

		This method can be improved for performance. Instread of iterating over 
		all juniors, propagate until deffered_user_label of a node change.

		param acl = [<UserLabel instance>, ...]
	'''
	def propagate_inferred_label(self, acl):
		immediate_juniors = self.is_senior_to
		for jnr_lbl in iter(immediate_juniors):
			jnr_lbl.inferred_user_label = acl
			acl = jnr_lbl.acl
			jnr_lbl.propagate_inferred_label(acl)

		

		
	
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
		if self.find_node(x) == None:
			self._add_2_nodes(x)
		if self.find_node(y) == None:
			self._add_2_nodes(y)

		xx = self.find_node(x)
		yy = self.find_node(y)
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
		
	
	def find_node(self,x_v):
		
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

class Configuration(object):
	def __init__(self):
		pass

	@staticmethod
	def _dummy_policy():
		return  [ ("o1","u1"), ("o2","u2") ]
	@staticmethod
	def _dummy_user_label():
		return [	("u1",["u2"]), \
				("u2",["u3"]), \
				("u3",[]) \
		       ]
	@staticmethod
	def _dummy_object_label():		
		return [	("o1",["o2"]), \
				("o2",["o3"]), \
				("o3",[]) \
		       ]

	def get_policy(self):
		pass


class Setup(object):
	def __init__(self):
		self._object_hierarchy = None
		self._user_hierarchy = None
		self._policy = None
		pass
	@property	
	def object_hierarchy(self):
		return self._object_hierarchy

	@object_hierarchy.setter
	def object_hierarchy(self, hrchy):
		self._object_hierarchy = LabelHierarchy(user=False) 
		try:
			for l_tuple in hrchy:
				(label,domination_list) = l_tuple
				for dl in domination_list:
					self._object_hierarchy.add_x_dominates_y(x=label,y=dl)
					pass

		except Exception as e:
			print e

	@property
	def user_hierarchy(self):
		return self._user_hierarchy

	@user_hierarchy.setter
	def user_hierarchy(self, hrchy):
		self._user_hierarchy = LabelHierarchy(user=True)
		try:
			for l_tuple in hrchy:
				(label,domination_list) = l_tuple
				for dl in domination_list:
					self._user_hierarchy.add_x_dominates_y(x=label,y=dl)
					pass
		except Exception as e:
			print e

	def bind_objectLabel_with_userLabel(self):
		print self._policy
		for plcy in iter(self._policy):
			(ol,ul) = plcy
			#now setup acl with each object.
			ol_instance = self._object_hierarchy.find_node(ol)
			ul_instance = self._user_hierarchy.find_node(ul)

			ol_instance.cleared_user_label = ul_instance
			ol_instance.inferred_user_label = ul_instance.all_senior_labels()
			# propagating acl of a object_label to all its junior object labels.
			ol_instance.propagate()
	
	'''
		get acl of all object_labels
		return a dictionary {'o_label':[u_label,...], ... } 
	'''
	@property
	def acl(self):		
		all_o_labels = self._object_hierarchy.labels
		acl_dict= {}
		for o_label in iter(all_o_labels):
			acl_dict[o_label.name] =  [ l.name for l in o_label.acl ]
		return acl_dict
	
		
	@property
	def policy(self):
		return self._policy
	'''	
		param  plcy : [ ("o1","u1"), ... ]
	'''
	@policy.setter
	def policy(self,plcy):
		self._policy = plcy
		self.bind_objectLabel_with_userLabel()

class AccessControl(object):
	def __init__(object):
		pass
	

def test_setup():
	setup = Setup()
	setup.object_hierarchy = Configuration._dummy_object_label()
	setup.user_hierarchy = Configuration._dummy_user_label()
	setup.policy = Configuration._dummy_policy()
	print setup.acl

def test_configuration():
	print "{} \n {} \n {} \n".format ( \
			Configuration._dummy_policy(), \
			Configuration._dummy_user_label(),\
			Configuration._dummy_object_label()     )



#status = working			
def test_user_label_hierarchy():
	ulh = LabelHierarchy(user=True)
	ulh.add_x_dominates_y(x="u1",y="u2")
	ulh.add_x_dominates_y(x="u2",y="u3")
	ulh.get_hierarchy()

#status= working
def test_object_hierarchy():
	olh = LabelHierarchy()
	olh.add_x_dominates_y(x="o1",y="o2")
	olh.add_x_dominates_y(x="o2",y="o3")
	olh.get_hierarchy()

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
	test_setup()
