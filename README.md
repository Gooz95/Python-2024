# GymGo website

## Imports
You need to install install psycopg2 and flask.

## Database set up
To use the website you need to set up a PostGreSQL database using any application you typically use, however I found issues using Docker Desktop to host the database as the database name could not be found despite being correct details. Any other application like pgAdmin 4 is perfectly usable.
After creating a fresh database you will need the database name, database user, database password, hostname, and port number. The default port PostgreSQL databases use is 5432 and if using pgAdmin 4 then the username is default 'postgres'.
Once you have these details you need to go to the *'siwel_files'* folder and run the *'db_init.py'* file. Use the 'Other' option and follow the prompts. This should print the results of a test prompt if successeful, if unsuccessful this is a problem with your database.
After the database is now set up you need to add it as the database that the website will connect to in *'siwel.py'* which is in the same folder as *'db_init.py'*. On line 9 in *'siwel.py'* there is the create_connection function, fill in the database, user, password, host, and port parameters with the same you entered in *'db_init.py'*.
Save your changes and now the website is good to go. 


## How to run the website
In the parent directory run the *'app.py'* file.
