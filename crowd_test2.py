import requests
from lxml import objectify

AUTH_USER="pam_client"
AUTH_PASS="SuperSecure"
URL_ROOT="http://192.168.1.101:8095/crowd/rest/usermanagement/latest/"

username = "pamtest"
#r = requests.get(URL_ROOT+"user.json?username=%s"% username, auth=(AUTH_USER,AUTH_PASS))
#print r.status_code, r.json()

password="passwordi"
data_obj = """<?xml version="1.0" encoding="UTF-8"?>
<password>
  <value>%s</value>
</password>""" % password
headers = {'content-type': 'application/xml'}
p = requests.post(URL_ROOT+"authentication?username=%s" % username, data=data_obj, auth=(AUTH_USER,AUTH_PASS), headers=headers)
print p.status_code, p.content
try:
  x = objectify.fromstring(p.content)
except Exception, e:
  print e.msg

if p.status_code == 200:
  print x.active
  if x.active:
    print "OK"
    print "Welcome, %s %s"% (x['first-name'], x['last-name'])
  else:
    print "FAIL"
elif p.status_code == 400:
  if x.reason=="USER_NOT_FOUND":
    print "PAM_USER_UNKNOWN"
  elif x.reason=="INVALID_USER_AUTHENTICATION":
    print "PAM_AUTH_ERR"


