# Dangerous apps Deauth
Discord tool to deauth sketchy apps

I made this tool in a couple of hours to help me deauthorize apps with the "join servers for you" permission which is often both dangerous and annoying, as bots can add you to NSFW/Scam servers.
Please open an issue if you enconter any errors, suggestions or other things! Or even if you want to suggest a MOTD.
(the motd switches to a random pyjoke if not set after a day)

# Setup guide for Linux
Clone the repository:

`git clone https://github.com/Natix1/DangerousAppsDeauth.git`

Open it:

`cd DangerousAppsDeauth`

Create a virtual environemnt

`python3 -m venv venv`

And activate

`source ./venv/bin/activate`

# Setup guide for Windows

Clone the repository

`git clone https://github.com/Natix1/DangerousAppsDeauth.git`

Open it:

`cd DangerousAppsDeauth`

Create a virtual environemnt

`python -m venv venv`

And activate

`.\venv\bin\activate.bat`

now, you can do

`pip install requirements.txt`

to install required libraries
and tada! youre done with the setup
to run, do
`python main.py`
common issue:
after closing the console and reopening it you need to activate the virtual environment. seems simple but the ammount of times i forgot is crazy.
