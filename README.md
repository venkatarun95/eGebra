eGebra
======

A front end for popular computer algebra systems which aims to replace traditional 'pen and paper' based symbolic mathematical manipulations

For more details about eGebra, see about.pdf in the Docs folder. To know how to run eGebra, read on.

Running eGebra
==============
The eGebra server is based on python-django. To run the debugging version of the server, navigate to the folder with 'manage.py' and type "python manage.py runserver" in the command line. Then open a browser and type "http://localhost:8000/egebra/login" in the address bar. Hopefully you should see a login screen. The only user in the database included is 'admin' whose password is also 'admin'.

Enjoy!

Code Documentation
==================

Common Conventions:

Docstrings are written whenever relevant closely following the practices recommended in:  https://www.python.org/dev/peps/pep-0257/

Naming conventions:
	Methods:
		Normal: camelCase
		Page 'view' handlers in views.py: camel_case_request
		Request handlers in views.py: camelCase_request
	Classes: 
		In cas_manager: camel_case
		In egebraServer: camelCase
	Variables: camelCase

Other Conventions:
	import: In any module, imports from standard python modules are placed at the top, separated by a single line by imports from modules that are a part of the eGebra system.
