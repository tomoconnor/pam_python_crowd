import requests
from lxml import objectify
import syslog
AUTH_USER="pam_client"
AUTH_PASS="SuperSecure"
URL_ROOT="http://192.168.1.101:8095/crowd/rest/usermanagement/latest/"

headers = {'content-type': 'application/xml'}

def auth_log(msg):
  syslog.openlog(facility=syslog.LOG_AUTH)
  syslog.syslog("pam_python.so %s" % msg)
  syslog.closelog()


def pam_sm_authenticate(pamh, flags, argv):
  try:
    user = pamh.get_user(None)
  except pamh.exception, e:
    return e.pam_result
  if not user:
    return pamh.PAM_USER_UNKNOWN
  try:
    resp = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "%s's Password:"%user))
  except pamh.exception, e:
    return e.pam_result

  try:
    data_obj = """<?xml version="1.0" encoding="UTF-8"?><password><value>%s</value></password>""" % resp.resp
    crowd_auth = requests.post(URL_ROOT+"authentication?username=%s" % user, data=data_obj, auth=(AUTH_USER,AUTH_PASS), headers=headers)
  except requests.exceptions.RequestException, e:
    return pamh.PAM_SYSTEM_ERR
  try:
    xml_content = objectify.fromstring(crowd_auth.content)
    if crowd_auth.status_code == 200:
      if xml_content.active:
        print "Welcome, %s %s" % (xml_content['first-name'], xml_content['last-name'])
        auth_log("%s %s Logged In"% (xml_content['first-name'], xml_content['last-name']))
        return pamh.PAM_SUCCESS
      else:
        return pamh.PAM_ACCT_EXPIRED 
    elif crowd_auth.status_code == 400:
      if xml_content.reason == "USER_NOT_FOUND":
        return pamh.PAM_USER_UNKNOWN
      elif xml_content.reason == "INVALID_USER_AUTHENTICATION":
        return pamh.PAM_AUTH_ERR 
      else:
        return pamh.PAM_SERVICE_ERR
    else:
      return pamh.PAM_SERVICE_ERR
  except Exception, e:
    auth_log(e.msg)
    return pamh.PAM_SYSTEM_ERR

def pam_sm_setcred(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
  return pamh.PAM_SUCCESS
