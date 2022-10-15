import re
import os
import slack_bolt
import os.path
import dotenv
import json
import random

from utils import is_greeting, is_anything, is_coinflip, is_help, quarter_heads, is_branding, quarter_tails, \
    text_block, is_acronym, ACRONYMS, BRANDING_RESPONSE, is_all_acronym

help_list = []
# Set up dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Initializes the app with the bot token and signing secret
app = slack_bolt.App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


# Greeting
@app.event(
    "app_mention",
    matchers=[lambda event: bool(is_greeting.search(event['text']))]
)
@app.message(is_greeting)
def greetings(say, context):
    """👋 `hi`, `hey`, `yo`, etc.: I can respond to these greetings, and more!"""
    random.seed()
    greeting = random.choice(["Hi", "Hey", "Yo", "Hello"])
    say(f"{greeting} <@{context['user_id']}>!")


help_list.append(greetings.__doc__)



# Greeting
@app.event(
    "app_mention",
    matchers=[lambda event: bool(is_acronym.search(event['text']))]
)
@app.message(is_acronym)
def acronym_search(say, event):
    """🤷 `What does SIG stand for?`, `list`: I can help you learn common acronyms in our field."""
    if 'text' in event:
        match_groups = is_acronym.search(event['text'])
        acronym = match_groups.group(2)
        if acronym in ACRONYMS:
            say(f"{acronym}: {ACRONYMS[acronym]}")
        else:
            say(f"Sorry, I don't know what `{acronym}` stands for, but you might find a definition "
                f"<https://www.acronymfinder.com/{acronym}.html|here>.")
    else:
        event_string = json.dumps(event, default=lambda x: "[[ Cannot be serialized ]]", indent="\t")
        raw_json = {
            "blocks": [text_block("Sorry, but I have no idea what you mean. Can you try to ask it in a different way? "
                                  "Here's what I saw: ")]
        }
        raw_json['blocks'].append(text_block(f"```event = {event_string}```"))
        say(raw_json)


help_list.append(acronym_search.__doc__)



# Greeting
@app.event(
    "app_mention",
    matchers=[lambda event: bool(is_all_acronym.search(event['text']))]
)
@app.message(is_all_acronym)
def all_acronyms(say):
    raw_json = {
        "blocks": [text_block("Here are all of the acronyms I know")]
    }

    sortednames = sorted(ACRONYMS.keys(), key=lambda x: x.lower())

    for key in sortednames:
        raw_json['blocks'].append(text_block(f"{key}: {ACRONYMS[key]}"))
    say(raw_json)



@app.event(
    "app_mention",
    matchers=[lambda event: bool(is_branding.search(event['text']))]
)
@app.message(is_branding)
def branding(say, context):
    """🌠 `brand`, `logo`, `font`: I'll return useful links for the lab brand."""
    say(BRANDING_RESPONSE)


help_list.append(branding.__doc__)


# Flip a coin and show result as image
@app.event(
    "app_mention",
    matchers=[lambda event: bool(is_coinflip.search(event['text']))]
)
@app.message(is_coinflip)
def ask_who(say):
    """🪙 `flip`, `coin`, `quarter`: I will flip a coin for you."""
    random.seed()
    if random.random() < 0.5:
        say(json.loads(quarter_heads))
    else:
        say(json.loads(quarter_tails))


help_list.append(ask_who.__doc__)


# Show structure of a string message
@app.event(
    "app_mention",
    matchers=[lambda event: bool(is_help.search(event['text']))]
)
@app.message(is_help)
def dump_help(say):
    """ℹ️ `about`, `help`, `info`: I will print this help table."""
    raw_json = {
        "blocks": [text_block("Here are a few of the things I can do!")]
    }
    for help_string in help_list:
        raw_json['blocks'].append(text_block(help_string))
    say(raw_json)


help_list.append(dump_help.__doc__)


# Catch all at the end and admit that it don't make no sense
@app.event("app_mention")
@app.message(is_anything)
def last_resort(context, say, message):
    """🤔`asdfasdf`, `kjnkjlkjb`, etc.: When you stop making sense, I'll let you know"""
    context_jstring = json.dumps(context, default=lambda x: "[[ Cannot be serialized ]]", indent="\t")
    message_jstring = json.dumps(message, indent="\t")
    raw_json = {
        "blocks": [text_block("Sorry, but I have no idea what you mean. Can you try to ask it in a different way? "
                              "Here's what I saw: ")]
    }
    raw_json['blocks'].append(text_block(f"```context = {context_jstring}```"))
    raw_json['blocks'].append(text_block(f"```message = {message_jstring}```"))
    say(raw_json)


help_list.append(last_resort.__doc__)

# Start the app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
