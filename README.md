Swift
=====
Swift with Content filter....

Step by step demo:

1. add Jsonpolicy with json file at object store.
	curl -X POST -H "X-Auth-Token:$TOKEN" -H 'X-Object-Meta-jsonpolicy:[ { "label":"protected", "target":"//past_employment" }, { "label":"public", "taget":"/" }, { "label":"protected", "target":"/personalRecord/identification" } ]' $STORAGE_URL/bar/employee.json

	- check the new meta name 'jsonpolicy'. It must the same for working.

2. Check if the meta is set properly:
	swift stat bar employee.json

3. GET request for the file
	curl -i -X GET -H "X-Auth-Token:$TOKEN" $STORAGE_URL/bar/employee.json


Note: the metadata can only be 256 character long. Need to find better way to store policy file.
