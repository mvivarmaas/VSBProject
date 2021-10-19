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
