# UpdateLoopiaIP
Python script for updating the IP address of the zone record for Loopia DNS

Run periodically on the server to ensure that the external IP on the Loopia DNS zone record matches the external IP, used when the server does not have a static external IP address.  

Uses a config file for credentials, alternatively modify to hardcode credentials. Credentials are not the same as the normal loopia login and have to be created in the loopia api section of the customer zone.
