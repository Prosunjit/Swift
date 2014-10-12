from lexical_analyzer import LexicalAnalyzer
from PythonJsonObj import PyObjTree, PyJSOb
import constant as constant
import utility as utl
import sys
import policy as Policy
from access_control import NodeHierarchy
from labac import Configuration, LBAC
import json

class ObQuery:
	def __init__(self, root_ob):
		self.tree_root = root_ob
		 

	def _gapvalue(self,gap_key, obj):
		r = []

		'''only object type has primitve member of {k:v} format. In Array object, primitive members are only string, or number. 
		so, need not to check prim_mem of array object '''

		if obj.type == "OBJECT":
			for o in obj.prim_mem:
				(k,v) =  o.items()[0]
				if k == gap_key:
					r.append(v)
		for o in obj.obj_mem:
			for (k,v) in o.items():
				if k == gap_key:
					r.append(v)
				else:
					r = r + self._gapvalue(gap_key,v)

		for o in obj.array_mem:
			if isinstance(o,PyJSOb):
				r = r + self._gapvalue(gap_key,o)
		return r
		pass	 
	def query(self,path):
		
		if path == "/":
			return [self.tree_root]
		path_token = LexicalAnalyzer(path).token_pair()
		ini_nodes = [self.tree_root]
		final_nodes=[]		
		token_pair = path_token

		for tp in token_pair:

			(t1,t2) = tp
			final_nodes = []
			 
			if t1 == "child":
				for root in ini_nodes:
					# looking into the object
					for n in root.obj_mem:
						for (k,v) in n.items():
							if k == t2:
								final_nodes.append(v)
					for n in root.prim_mem:
						(k,v) = n.items()[0]
						if k == t2:
							final_nodes.append(v)
				pass
				 
			elif t1 == "index":
				for root in ini_nodes:
					t2 = int(t2)
					try:
						n = root.array_mem[t2]
					except:
						pass
				final_nodes.append(n)
				pass
				 
			elif t1 == "gap":
				for root in ini_nodes:
					final_nodes = final_nodes + self._gapvalue(t2,root)
				pass
			ini_nodes = final_nodes
		return final_nodes

	
	def _authorized_only(self, job, cbac, user_clearance):
		# check descendant nodes for clearance
		r_obj = []
		if job.type == "OBJECT":
			# check for obj_members
			for ob in job.obj_mem:
				(key,value) = ob.items()[0]
				value = self._authorized_only(value,cbac, user_clearance)
				if value:
					r_obj = r_obj + [{key:value}] # if obj, pass key,value dictionary
			pass
		elif job.type == "ARRAY":
			
			for ar in job.array_mem:
				value = self._authorized_only(ar, cbac, user_clearance)
				if value:
					r_obj = r_obj + [value]
			pass
		else:
			pass
		
		'''some change required here'''

		# check if job is has clearance, a function shold be called here
		#if  job.label != constant.DEFAULT_LABEL and label_hierarchy.check(user_clearance,job.label) : 
		object_label = [job.label]


		if job.label != constant.DEFAULT_LABEL and cbac.request(action="read", user=user_clearance, object=object_label):

			#remove all existing array, ob members
			job.array_mem = []
			job.obj_mem = []

			# return None when a json obj has no member

			if len(r_obj) == 0 and len (job.prim_mem) == 0:
				return None

			for o in r_obj:
				if type(o) is dict:
					(k,v) = o.items()[0]
					job.add_obj_mem(key=k, value=v)
				else:
					job.add_array_mem(o)
			pass
			return job
		
		else:
			ob = PyJSOb()
			if len(r_obj) == 0:
				return None
			for mem in r_obj:
				if type(mem) == dict:
					(k,v) = mem.items()[0]
					ob.add_obj_mem(key=k, value = v)
				elif isinstance(mem,PyJSOb)  and mem.type == constant.ARRAY:
					ob.add_array_mem(mem)
			
			return ob
	

		
		


	# this method do query without ac, then apply access control on the result
	# not considering clearance lattice.

	def ac_query(self, path, cbac, user_clearance):
		q_res = self.query(path)
		authorized_list = []
		print q_res
		for ob in q_res:
			authorized_list.append( self._authorized_only(ob, cbac, user_clearance))
			pass

		return authorized_list
		pass

class UserHierarchy:
	def __init__(self):
		pass
	def get_hierarchy(self):				
		nh = NodeHierarchy()
		nh.insert("private","public")
		nh.insert("protected","private")
		return nh


class CBAC:
	@staticmethod
	def get(file_in_json=None):
		
		print file_in_json
		#file_in_json = LoadJSON(str=).get_json()
		
		if file_in_json:
			user_labels = file_in_json['user_labels']
			object_labels = file_in_json['object_labels']
			policy = file_in_json['policy']

			conf = Configuration()
			u_ls = []
			o_ls = []
			for ul in user_labels:
				t = (str(ul['name']), [str(i) for i in ul['dominates']] )
				u_ls += [t]

			for ol in object_labels:
				t = (str(ol['name']), [str(i) for i in ol['dominates']])
				o_ls += [t]

			read_policy = policy['read']
			r_p = []
			for p in read_policy:
				t = (str(p['object_label']), str(p['user_label']))
				r_p += [t]
			
			conf.object_label_hierarchy = o_ls
			conf.user_label_hierarchy  = u_ls
			conf.add_policy("read",r_p)
			

			lbac = LBAC(conf)
			return lbac

class ContentFilter:
	def __init__(self, content_file=None, content_str=None, \
		    labeling_policy_file=None, labeling_policy_str=None, cbac_policy=None, query=None, user_clearance=None):
		self.content_file = content_file
		self.content_str = content_str
		self.policy_file = labeling_policy_file
		self.policy_str = labeling_policy_str
		self.JSONPath = query
		self.user_clearance = user_clearance
		self.cbac_policy = cbac_policy

		#print "debug------"
		#print locals()
		
	def apply(self):

		# ---- Build JSON tree -------#

		print "flg0"
		if self.content_file:			 
			obj_tree = PyObjTree(utl.LoadJSON(path=self.content_file).get_json()).get_root()
		elif self.content_str:
			obj_tree = PyObjTree(utl.LoadJSON(str=self.content_str).get_json()).get_root()
		# ------- Label JSON tree with object labels -------#
		if self.policy_file:
			obj_tree = Policy.NodeLabeling(obj_tree,label_str=utl.File(self.policy_file).read()).appy_labels()
		elif self.policy_str:	
			print self.policy_str
			obj_tree = Policy.NodeLabeling(obj_tree,label_str=self.policy_str).appy_labels()
		# ---- get uer Hierarchy ------#
		#hierarchy = UserHierarchy().get_hierarchy()	
		print "flg1"
		#print self.cbac_policy

		'''cbac_policy was a dictionary, converting it to string by json.dumps then again
		returning it to json format by json.loads'''
		print "1.2"
		print self.cbac_policy
		self.cbac_policy = json.dumps(self.cbac_policy)
		self.cbac_json = json.loads(self.cbac_policy)

		print self.cbac_json

		cbac = CBAC.get(file_in_json=self.cbac_json)	
		
		print "flg1.5"

		# --- Work with Query class for Querying --- #
		oq = ObQuery(obj_tree)
		
		print "flg2"

		self.JSONPath = self.JSONPath if self.JSONPath else '/'
		qry = [self.JSONPath]

		for q in qry:
			if self.user_clearance : # if user_clearance is given, user hiearchy is used.
				res = oq.ac_query(q, cbac, self.user_clearance)
			else: # if user clearance is not given just use the JSONPath to query.
				res = oq.query(q)
			# we need to iterate through the res. there can be more than one result.
			for r in res:
				if type(r) is dict:
					(k,v) = r.items()[0]
					return   utl.pretty_print ( v.print_json() )
					pass
				elif isinstance(r,PyJSOb):
					#print r.print_json()
					return  utl.pretty_print ( r.print_json() )
				else:
					return  r
	

def test1():
	print  ContentFilter(content_file="employee.json", policy_file="path_label_policy.json",\
	query="/personalRecord",user_clearance="protected").apply()

def test():
	
	#run with this command :  python ObQuery.py employee.json /personalRecord

	#build the Json Obj tree here
	#obj_tree = PyObjTree(utl.LoadJSON(path=sys.argv[1]).get_json()).get_root()
	obj_tree = PyObjTree(utl.LoadJSON(str=utl.File(sys.argv[1]).read()).get_json()).get_root()
	#apply labels to obj tree
	#obj_tree = Policy.NodeLabeling(obj_tree,label_file="path_label_policy.json").appy_labels()

	obj_tree = Policy.NodeLabeling(obj_tree,label_str=utl.File("path_label_policy.json").read()).appy_labels()


	path = sys.argv[2]

	nh = NodeHierarchy()
	nh.insert("private","public")
	nh.insert("protected","private")


	oq = ObQuery(obj_tree)

	qry = [path]

	for q in qry: 
	
		if len(sys.argv) >=4 :
			res = oq.ac_query(q,nh,sys.argv[3])
		else:
			res = oq.query(q)
		# we need to iterate through the res. there can be more than one result.
		for r in res:
			#print r
			if type(r) is dict:
				(k,v) = r.items()[0]
				print utl.pretty_print ( v.print_json() )
				pass
			elif isinstance(r,PyJSOb):
				#print r.print_json()
				print utl.pretty_print ( r.print_json() )
			else:
				print r
	

def test_cbac():
		
	user_labels = '[{"dominates": ["employee"], "name": "manager"}, {"dominates": ["stuff"], "name": "employee"}]'
	object_labels = '[{"dominates": ["public"], "name": "protected"}, {"dominates": ["public"], "name": "private"}]'
	json_policy = '{"read": [{"user_label": "manager", "object_label": "protected"}, {"user_label": "employee", "object_label": "private"}]}'
	object_labelling = '[{"target": "/", "label": "protected"}, {"target": "/personalabelRecord", "label": "public"}]'

	cbac_policy = {}
	cbac_policy['user_labels'] = json.loads(user_labels)
	cbac_policy['object_labels'] = json.loads(object_labels)
	cbac_policy['policy'] = json.loads(json_policy)

	user_clearance = ['employee']
	jsonpath = "/"
	
	if True:
		if json_policy and user_clearance and jsonpath and object_labelling:
			filtered_content = ContentFilter(content_str= utl.File('employee.json').read(),\
			labeling_policy_str=object_labelling, \
			user_clearance=user_clearance, query=jsonpath, \
			cbac_policy=cbac_policy).apply()
			
			
			print ">>", filtered_content


if __name__ == "__main__":
	test_cbac()
