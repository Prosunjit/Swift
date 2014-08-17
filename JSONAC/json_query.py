import sys
import json
from  lexical_analyzer import LexicalAnalyzer
from access_control import Policy
import utility as  utility

class Query:
	def __init__(self,json,t):
		self.json = json
		self.token_pair = t
		self.cur = {}	# all the json obs are in cur before running query
		#self.cur.append(json)
		self.cur = json
		self.jobaq = {} # holds json objects after running a query
		#print json
		#print t

	def _gapvalue(self,gap_key, obj):
		result = []
		if type(obj) is list:
			for o in obj:
				result = result + self._gapvalue(gap_key,o)
			return result
		elif type(obj) is dict:
			#obj is of type instance/object
			for (k,v) in obj.items():
				if k == gap_key:
					result.append(v)
				else:
					result = result + self._gapvalue(gap_key,v)
			return result
		else:
			return []

	def execute(self):
		
		token_pair = self.token_pair
		cur = self.cur
		jobaq = self.jobaq
		
		for tp in token_pair:
			(t1,t2) = tp
			#print t1, t2
			if t1 == "child":
				for (key, j_ob) in cur.items(): # for j_ob in the current jsobob list in cur...
					n_ob = j_ob[t2]
					# need to check the policy here.
					if Policy().enforce("public","public") == True:
						#self.jobaq.append(n_ob)
						jobaq[t2] = n_ob
			elif t1 == "index":
				print "...."
				print cur
				for  key in cur:
					j_ob = cur[key]
					n_ob = j_ob[int(t2)]
					if Policy().enforce("public","public") == True:
						#self.jobaq.append(n_ob)
						jobaq[t2] = n_ob
			elif t1 == "gap":
				gapvalues=[]
				for (key,j_ob) in cur.items():
					
					if key == t2:
						gapvalues  = gapvalues + [j_ob]
					else:
						gapvalues  = gapvalues +  self._gapvalue(t2,j_ob)
				jobaq[t2] = gapvalues;

						
			cur = jobaq
			jobaq = {}
		return cur





def test():
	jsonpath = sys.argv[1]
	label = sys.argv[2] 
	print "jsonpath:" + jsonpath
	lj = utility.LoadJSON("employee.json")
	j =  lj.get_json()
	#print j
	#print x["personalRecord"]["name"]
	la = LexicalAnalyzer(jsonpath)
	token_p = la.token_pair()
	q = Query({"data":j},token_p)
	print json.dumps( q.execute(), indent=4, sort_keys=True)

	filtered_content =  Policy().keep_label(q.execute(),label,[])
	print json.dumps(filtered_content, indent=4, sort_keys=True)

	#print x.get("name")
	#print lj.data

test()
