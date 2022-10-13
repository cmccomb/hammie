import re
import random

# Matches for checking
is_greeting = re.compile("(hi|hello|hey|yo)", re.IGNORECASE)
is_anything = re.compile(".*")
is_coinflip = re.compile("(flip|coin|quarter)")
is_help = re.compile("(help|about|info)")
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
