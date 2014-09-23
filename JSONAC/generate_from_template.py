import utility as utl

NO_OF_ITER=3

def test_generate():
	return generate_with_template("employee.template")


def generate_with_template(template):
	bigfile=""
	for i in range(1,NO_OF_ITER):
		emp_no = "employee_"+ str(i)
		opt_separator = "" if i==1 else ","
		bigfile += opt_separator +  "\"{}\":{}".format(emp_no, utl.File(template).read())

	return "{" +  bigfile + "}" 

if __name__ == "__main__":
	print test_generate()
	pass
