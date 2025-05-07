# Contacts Application
A project I developed for one of my software integration courses!
## What is it?
This application is a simple implementation of a contacts app. Using my VCard parser library I developed in an earlier iteration of this project, I integrated the shared library that parses VCard file formats into a more simple format to work with. I used the library as my back end and added more helper functions to integrate to the Ctypes library in python where I used asciimatics which is a TUI. This application also dabbled into databases thus there is a login page to connect to the database. But, this database is hosted by my faculty so unfortunately, users will not be able to access the database features unless they have one with University of Guelph, School of Computer Science. Regardless, this project demonstrates a simple overview of how the VCard parser library can be applied to other projects.

## How to use it
I would have some VCard files loaded into the cards folder within my bin folder. Within the command line, run "make". Then access the bin folder path, run "python3 A3Main.py" to run the application. It'll be an old school UI where you can either login with your database credentials or click cancel to not connect to the database.

## Note
Note that for the file modification and creation time is in UTC according to when the file is changed. I chose to use the os.path.getmtime() for both columns in the sql query instead of NOW(). With os.path.getmtime() the time in UTC is ahead of EST by 4 hours so the queries will have a different time zone. For the June query, I was unsure of how to handle the DATEDIFF()/365 since it could be rounded, so if ages differ by seconds it may not be reflected.
