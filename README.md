pam_python_crowd
================

Requirements
------------

* pam_python (I used the version from the ubuntu repositories)
* pam_exec (to run the script to add the user when they login the first time).
* Atlassian Crowd 2.1 (That's the version I used).

1. Copy `usr/share/pam-configs/pam_config_python` into `/usr/share/pam-configs`
1. Create a generic Application in Crowd, remember the application name and password for the next step.
1. Edit lib/security/pam_crowd.py to set your crowd server's URL and application auth tokens.
1. Install the python modules `lxml` and `requests`.
1. Edit `crowd_test2.py` and `crowd_test.py` to match the server url and auth tokens (for testing).
1. Copy `usr/local/bin/mkuser` to `/usr/local/bin`
2. Run `pam-auth-update` and enable "PAM_Python Module with pam_crowd.py".  Save the config.
1. Add `session required pam_exec.so /usr/local/bin/mkuser` to the top of `/etc/pam.d/common-session`
1. Create a user in Crowd, and try logging in as them (should work as a native TTY login, or even ssh!)

