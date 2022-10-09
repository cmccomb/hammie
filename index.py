import re
import os
import slack_bolt
import os.path
import dotenv
import json
import random

NAME = "Hammie"

help_list = []
# Set up dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Initializes the app with the bot token and signing secret
app = slack_bolt.App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


# Basic greeting
@app.message(re.compile("(hi|hello|hey|yo)", re.IGNORECASE))
def greetings(say, context):
    """
    I can respond to a variety of casual greetings, including hi, hello, hey, and yo.
    """
    greeting = context['matches'][0]
    print(context)
    say(f"{greeting} <@{context['user_id']}>!")


help_list.append(help(greetings))


# Flip a coin and show result as image
@app.message("flip a coin")
def ask_who(message, say):
    if random.random() < 0.5:
        say(json.loads(
            """
                {
                    "blocks": [
                        {
                            "type": "image",
                            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/2006_Quarter_Proof.png/780px-2006_Quarter_Proof.png",
                            "alt_text": "heads"
                        }
                    ]
                }
            """
        ))
    else:
        say(json.loads(
            """
                {
                    "blocks": [
                        {
                            "type": "image",
                            "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/1999_PA_Proof.png",
                            "alt_text": "tails"
                        }
                    ]
                }
            """
        ))


# Show structure of a regex context
@app.message(re.compile("^(debug_regex)"))
def debug_regex(say, context):
    jstring = json.dumps(context, default=lambda x: "[[ Cannot be serialized ]]", indent="\t")
    say(f"```{jstring}```")


# Show structure of a string message
@app.message("debug_string")
def debug_string(message, say):
    jstring = json.dumps(message, indent="\t")
    say(f"```{jstring}```")


# Show structure of a string message
@app.message("help")
def dump_help(message, say):
    jstring = json.dumps(help_list, indent="\t")
    say(f"```{jstring}```")


# Catch all at the end and admit that it don't make no sense
@app.message(re.compile(".*"))
def last_resort(say, context):
    message = context['matches'][0]
    print(context)
    say(f"Sorry, but I have no idea what you mean by \"{message}\". Can you try to ask it in a different way?")


# Start the app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
