
class JSONOps:
	def __init__(self,jsonob):
		self.json_ob = jsonob
	
	def read(self):
		json = ""
		json = json + self.read_primitive_member()
		json = json + self.read_object_member()
		json = json + self.read_array_member()
		return json
	def read_primitive_member():
		
		pass
	def read_object_member():

		pass

	def read_array_member():

		pass
