# post_gen_bot
This is a little bit of a different bot than the ones I've previously made, in that, *this one* will read specifically from column C of spreadsheets obtained through Google's API, and your own Google Sheets. In my own instance, we're using spreadsheets of all of the Mastodon posts that I've made in a year, and then posting them jumbled and then reassembled, at random, to Mastodon. This requires a little bit of knowledge about how to obtain access to Google's API, and how to generate a key, and then download your credentials for Sheets.

How to set it up:

Firstly, you're going to want to have a server running, unless you just want to set this up and run it one time just to see how it goes. And then, you'll want to create a new environment for the bot, because you shouldn't just live in open deadspace (it's scary out there).

```
python3 -m venv post-gen-env
```

Next, activate the environment.
```
source post-gen-env/bin/activate
```
Now make a directory where the bot can live, and have coffee.
```
mkdir post-gen-bot
```
Pay the bot's new home a visit.
```
cd post-gen-bot
```
Make a requirements.txt in order to make the task of installing everything you need for the bot to run properly simpler.
```
nano requirements.txt 
```
and then insert the contents of the txt file from this repository.

Make a credentials directory where your bot can hide its keys.
```
mkdir creds
```
Open the door
```
cd creds
```
Copy/paste the name of your Google API credentials .json
```
nano name_of_your_cred_file.json
```
and then paste in the contents of *that* file.

Come out of the closet.
```
cd ..
```
Install the packages.
```
pip install -r requirements.txt
```
Create the bot!
```
nano post-gen.py
```
and then copy in the contents of the post-gen.py file here from the repository, make sure you edit the credentials path properly, and also your Mastodon URL and access key.

Run, just run, run far away, I ran so far awaaaayyyy, gotta get away?
```
python3 post-gen.py
```
It works?

Alright, now set us up the cronjob.
```
crontab -e
```
```
*/30 * * * * post-gen-env/bin/python3 post-gen-bot/post-gen.py
```
**You're done!**
