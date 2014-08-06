pam_python_crowd
================

This is a mechanism for logging into a Linux computer using Atlassian's Crowd authentication server.  I've only really tested it on Ubuntu 13.10, although it *ought* to work on any PAM-based system.

It's the result of a saturday's hacking, and is pretty much just a proof-of-concept, and probably ***Unwise to use in Production*** environments.

I really need to write a libnss module to allow `getpwname` to use Atlassian for retrieving user and group information.

Currently, if the user doesn't have a matching account in /etc/passwd, one will be created via potentially unsafe use of `pam_exec.so`.

NOTE: If the user doesn't yet exist locally, it will be created -- however, it will fail to auth until a second try at login. This is due to PAM not noticing when a user is created mid-authorization.

Requirements
------------

* pam_python (I used the version from the ubuntu repositories)
* pam_exec (to run the script to add the user when they login the first time).
* Atlassian Crowd 2.1 (That's the version I used).

1. Copy `usr/share/pam-configs/pam_config_python` into `/usr/share/pam-configs`
1. Create a generic Application in Crowd, remember the application name and password for the next step.
1. Edit lib/security/pam_crowd.py to set your crowd server's URL and application auth tokens.
1. Copy lib/security/pam_crowd.py to /lib/security
1. Install the python modules `lxml` and `requests`.
1. Edit `crowd_test2.py` and `crowd_test.py` to match the server url and auth tokens (for testing).
1. Copy `usr/local/bin/mkuser` to `/usr/local/bin`
1. Run `pam-auth-update` and enable "PAM_Python Module with pam_crowd.py".  Save the config.
1. Create a user in Crowd, and try logging in as them (should work as a native TTY login, or even ssh!)

