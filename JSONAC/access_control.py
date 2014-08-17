import utility as util
class Policy:

        def __init__(self):
                pass

        def enforce(self,req_label, cur_label):
                # assume no label hierarchy. Security policy need to be inforced here.
                if req_label != cur_label:
                        return False
                return True
	def check_label_policy(self,u_label, n_label):
		nh = NodeHierarchy()
		# label hierarcy poset should be fitted in the following line.
		nh._default_hierarchy_setup()
		return nh.check(u_label,n_label)

        def keep_label(self,node,label,white_nodes):
                ''' node is a dictionary of {k:ob} form , label is the access label, white_nodes are the nodes that have been cleared for access. on every run of these function, we traverse child dict, and find which nodes can be shown (in white_nodes). then from the current node, delete all teh object and insert only the white_objects.
                '''
		obj_array = False
                (k, v) = node.items()[0]
		
		#if v is an array / list, convert list into dict. set array=True
		if type(v) is list:
			v = util.list2Dict(v)
			obj_array = True

		# if v is a object(dict)
                for (key, value) in v.items():
                        if type(value) is dict:
                                tmp = self.keep_label({key:value}, label, [])
                                if tmp:
                                        for el in tmp:
                                                white_nodes.append(el)
			elif type(value) is list:
				pass
			else:
				pass

		if obj_array == True:
			print white_nodes
			return util.remove_key_from_dict_array(white_nodes)

		# if arrray == True:

                #if "label" in v and v["label"] == label:
		if "label" in v and self.check_label_policy(label,v["label"]) :
                        #remove objects that are not in whitelist
                        delete_obj=[]
                        for key, value in v.iteritems():
                                if type(value) is dict:
                                        delete_obj.append(key)
                        for item in delete_obj:
                                del(v[item])
                        # delete the label node from output
                        del(v['label'])
                        # needs more work here.
                        if white_nodes:
                                for wn in white_nodes:
                                        if wn:
                                                (_k,_item) =  wn.items()[0]
                                                v[_k] = _item
                                return [{k:v}]
                        else:
                                return [{k:v}]
                else:
                        return white_nodes;


'''
	Hierarchy node has node of type treenode.
'''

class TreeNode:
	def __init__(self,name):
		self.children = []
		self.value = name
	
	def add_child(self, tn):
		self.children.append(tn)

'''
	access label hierarchy. This is essentially a partial order.

'''

class NodeHierarchy:
	def __init__(self):
		# all the root of the partial order set is stored in root_list
		self.root_list = []
		# all nodes of the Node Hierarchy
		self.nodes=[]

	def _default_hierarchy_setup(self):

		self.insert("private","public")
		self.insert("protected","private")

	def insert(self,x_v,y_v): # insert a hierarchy of two node such that x dominates y. x_v, y_v are values of x & y
		if self._find_node(x_v) == None:
			self._add_2_nodes(x_v)
		if self._find_node(y_v) == None:
			self._add_2_nodes(y_v)

		x = self._find_node(x_v)
		y = self._find_node(y_v)
		x.add_child(y)

	def check(self,x_v,y_v): # check there x dominates y
		
		x = self._find_node(x_v)
		y = self._find_node(y_v)
		status = False

		if x_v == y_v:
			return True

		for n in x.children:
			status= self.check(n.value,y_v)
			if status ==  True:
				return status
		return False

	def _add_2_nodes(self,x_v):
		tn = TreeNode(x_v)
		self.nodes.append(tn)
		
	
	def _find_node(self,x_v):
		
		for n in self.nodes:
			if n.value == x_v:
				return n
		return None

	
		
def test():
	nh = NodeHierarchy()
	#nh._add_2_nodes("public")
	#nh._add_2_nodes("private")
	#print nh._find_node("public")
	nh.insert("private","public")
	nh.insert("protected","private")
	print nh.check("protected","public")

if __name__ == "__main__":
	test()
