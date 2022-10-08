import re
import os
import slack_bolt
from os.path import join, dirname
from dotenv import load_dotenv
import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Initializes your app with your bot token and signing secret
app = slack_bolt.App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.message(re.compile("(hi|hello|hey)"))
def say_hello_regex(say, context):
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")

    
@app.message("knock knock")
def ask_who(message, say):
    say("_Who's there?_")
    
    
@app.message(re.compile("^debug_regex"))
def debug(say, context):
  say(json.dumps(context))
  
    
@app.message("debug_string")
def debug(message, say):
  say(json.dumps(message))

    
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
