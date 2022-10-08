import re
import os
import slack_bolt
import os.path
import dotenv
import json
import random

# Set up dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Initializes your app with your bot token and signing secret
app = slack_bolt.App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.message(re.compile("(hi|hello|hey)"))
def say_hello_regex(say, context):
    greeting = context['matches'][0]
    print(context)
    say(f"{greeting}, how are you?")



@app.message("flip a coin")
def ask_who(message, say):
    if random.random() < 0.5:
        say(json.loads(
            """
                {
                    "blocks": [
                        {
                            "type": "image",
                            "image_url": "https://www.usmint.gov/wordpress/wp-content/uploads/2021/12/2022-american-women-quarters-coin-uncirculated-obverse-philadelphia-768x768.jpg",
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
                            "image_url": "https://www.usmint.gov/wordpress/wp-content/uploads/2021/12/2022-american-women-quarters-coin-sally-ride-uncirculated-reverse-768x768.jpg",
                            "alt_text": "tails"
                        }
                    ]
                }
            """
            ))
    
    
@app.message(re.compile("^(debug_regex)"))
def debug_regex(say, context):
    context['logger'] = ''
    say(json.dumps(context))
  
    
@app.message("debug_string")
def debug_string(message, say):
    say(json.dumps(message))

    
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
