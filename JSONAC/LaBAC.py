'''
        Object label class. All the junior label of a label is maintained with 
	a label.
'''
class ObjectLabel(object):
	
	def __init__(self, name):
		# cleared_label  means the user label that have access this object label  as specified in the policy.
		self.cleared_u_label = []
		# inferred_label means inferred user labels that have access to this object label by user label hierarchy
		self.inferred_u_label = []
		# for object label we need all labels that are junior to a given label
		self.junior_labels = []	

	
	@property
        def is_senior_to(self):
                return self.junior_labels

	@is_senior_to.setter	
	def is_senior_to(self,label):
		self.junior_labels.append(label)

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
	test()
