Swift
=====
Swift with Content filter....

Step by step demo:

1. add Jsonpolicy with json file at object store.
	- curl -X POST -H "X-Auth-Token:$TOKEN" -H 'X-Object-Meta-jsonpolicy:[ { "label":"protected", "target":"//past_employment" }, { "label":"public", "taget":"/" }, { "label":"protected", "target":"/personalRecord/identification" } ]' $STORAGE_URL/bar/employee.json

	- check the new meta name 'jsonpolicy'. It must the same for working.

2. Check if the meta is set properly:
	- swift stat bar employee.json

3. GET request for the file
	- curl -i -X GET -H "X-Auth-Token:$TOKEN" $STORAGE_URL/bar/employee.json


Note: the metadata can only be 256 character long. Need to find better way to store policy file.



------------------------------------------------------------------------------
set-up keystone for the experiment:

* Adding a role 'protected and attaching it to user 'demo' of tenant 'demo' * :

- keystone --os-username=admin --os-password=nova role-create --name protected
- keystone --os-username=admin --os-password=nova user-role-add --user=demo --role=protected --tenant=demo
- keystone --os-username=admin --os-password=nova user-role-list --user=demo


--------------------------------------------------------------------------------

Set up $TOKEN & $STORAGE_URL for experiment

export TOKEN=`keystone token-get | grep id | head -n 1 | awk '{print $4}'`
s_url=`keystone --os-username=admin --os-password=nova endpoint-list | grep AUTH_ | awk '{print $6}' | sed 's/\$(tenant_id)s//'`
tenant_id=`keystone –os-username=admin –os-password=nova tenant-get $OS_TENANT_NAME | grep id | awk ‘{print $4}’`
export STORAGE_URL=$s_url$tenant_id
