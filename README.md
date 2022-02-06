this scrapes content from WP user pages
for it to work you have to install a few things
```
> pip install selenium
> pip install webdriver
> pip install selectorlib
> pip install python-dotenv
> pip install jsonlines
```
you also have to 
```
cp .env.sample .env
```
and change it to have your username and password.  Then
```
python 01_get_users.py
python 02_get_user_content.py
```
The site does have an immune response to selenium which creates so awkness. You'll have to manually click "submit" on the login page, and you might have to solve a captcha, and you'll have to close pop-ups maybe. right now it only pulls a few accounts, it's a demo to be extended. it only pulls a few page attributes.  by pulling accounts from the posts screen it over samples active users. to sample regular users increment through IDs, probably counting from about 40000 down.  There will be countermeasures to work aroundif you do this. 
