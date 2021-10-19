# freeseatfinder.com

The following is the code for freeseatfinder.com <b> Note an unexpected number of users joined and it became a bit too expensive to opperate without some code changes, with a bit of work the service will be back up again</b> 


##  How to deploy  
run the following commands

1. <code>git clone https://github.com/abubakardaud/VSBProject</code>
2. <code>cd VSBProject</code> If you have an IDE open this with an IDE or virtualenv
3. <code>pip3 install requirements.txt</code>
4. <code>python3 manage.py makemigrations</code>
5. <code>python3 manage.py migrate</code>
5. <code>python3 runserver</code>

## To do list in terms of priority 

1. Change the system schudule to ping VSB so we don't get rate limited; need to upgrade (django-background-tasks) 
2. Make sure the pings appear to look normal from google chrome
3. Change the CSS / HTML to make it more pretty
4. OAuth and accounts with McGill login so people can remove / add to the waitlist 
5. Introduce rate limits so users can't ping our servers hundreds of times in seconds
6. Introduce a cheaper Phone system 

## File structure  

├── _VSBProject (settings, don't edit unless you know what you are doing )
├── _mainpage (the main webpage itself is an app and it's hosted here)
│   ├── VSBLogic.py (has the code to reverse engineer the VSB API) 
|   ├── models.py (data base ORM models layout for the SQL data base) 
|   ├── urls.py (maps the URLs to views)
|   ├── views.py (functions that return a view to the client (HTML page etc))
|   └── tests.py (tests for the app need to write more functions)   
|   
├── _static (contains the static files, CSS Javascript)
├── _staticfiles (generated staticfiles by Django)
├── _templates
|   ├── 500.html (server error HTML)
|   ├── API.html (Api HTML code to show people how to use the API)
|   ├── account.html (Todo need to build an account page)
|   ├── base_template.html (Base template header and footer, everything else extends from this one, look up Django extend)
|   ├── contact.html (contact me using HTML)
|   ├── contactsuccess.html (contact success)
|   ├── fail.html (failed page for the process of finds class)
|   ├── index.html (landing page)
|   ├── no_crn.html (user didn't check a crn)
|   ├── results.html (pull the classes after look up from the index page 
|   └── success.html (added to the waitlist success for the user)
│   
│── Procfile (for heroku don't touch unless you know how to use Heroku)
|── README.md (this current text)
|── manage.py (Djnago file, read Djnago docs)
└── requirements.txt (has all the needed installs to make the project work ) 


