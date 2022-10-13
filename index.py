import re
import os
import slack_bolt
import os.path
import dotenv
import json
import random

NAME = "hammie"

help_list = []
# Set up dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Initializes the app with the bot token and signing secret
app = slack_bolt.App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Matches for checking
is_greeting = re.compile("(hi|hello|hey|yo)", re.IGNORECASE)
is_anything = re.compile(".*")
is_coinflip = re.compile("^(flip|coin|quarter)$")


# Textblock
def text_block(markdown_string):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": markdown_string
        }
    }

# Quarters
quarter_heads = """
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

quarter_tails = """
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


def is_hello(event) -> bool:
    return bool(is_greeting.search(event['text']))


@app.event("app_mention", matchers=[is_hello])
def hello_there(event, say):
    say("Hey there!")

@app.event("app_mention")
def app_mention_catchall(event, say):
    jstring = json.dumps(event, indent="\t")
    say(f"```{jstring}```")

# Basic greeting
@app.message(is_greeting)
def greetings(say, context):
    """👋 `hi`, `hey`, `yo`, etc.: I can respond to these greetings, and more!"""
    greeting = context['matches'][0]
    say(f"{greeting} <@{context['user_id']}>!")


help_list.append(greetings.__doc__)


# Flip a coin and show result as image
@app.message(is_coinflip)
def ask_who(say, context):
    """🪙 `flip`, `coin`, `quarter`: I will flip a coin for you."""
    if random.random() < 0.5:
        say(json.loads(quarter_heads))
    else:
        say(json.loads(quarter_tails))


help_list.append(ask_who.__doc__)


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
@app.message(re.compile("^(help|about|info)$"))
def dump_help(message, say):
    """ℹ️ `about`, `help`, `info`: I will print this help table."""
    raw_json = {
        "blocks": [text_block("Here are a few of the things I can do!")]
    }
    for help_string in help_list:
        raw_json['blocks'].append(text_block(help_string))
    say(json.loads(json.dumps(raw_json)))


help_list.append(dump_help.__doc__)


# Catch all at the end and admit that it don't make no sense
@app.message(is_anything)
def last_resort(say, context):
    message = context['matches'][0]
    print(context)
    say(f"Sorry, but I have no idea what you mean by \"{message}\". Can you try to ask it in a different way?")


x = (is_greeting, greetings)

# Start the app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
x