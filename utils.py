import re
import random

# Matches for checking
is_greeting = re.compile(r"\b(hi|hello|hey|yo)\b", re.IGNORECASE)
is_anything = re.compile(r".*")
is_coinflip = re.compile(r"\b(flip|coin|quarter)\b")
is_help = re.compile(r"\b(help|about|info)\b")
is_branding = re.compile(r"(brand|logo|font)")
is_acronym = re.compile(r"(w|W)hat does (?:[A-Z]){2,} stand for")

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

BRAND_BOOK_LINK = "https://cmu.box.com/shared/static/ag94ilmtc82y26plb8rdl4xw62qgglop.pdf"
FONTS_LINK = "https://cmu.box.com/shared/static/a4dwu8lvw6txhbe98vcd5naotsfe7ag1.zip"
LOGOS_LINK = "https://cmu.box.com/shared/static/1olz4zle4s4qdn5y4nu73fglz69mn131.zip"
ASSETS_LINK = "https://cmu.box.com/shared/static/oynnamlbyjxlmw9tqrqqb4b7d3kwg8w4.zip"

ACRONYMS = {
    "ASME": "American Society of Mechanical Engineers",
    "CIE": "Computers and Information in Engineering Conference",
    "IDETC": "International Design Engineering and Technical Conferences",
    "DAC": "Design Automation Conference, part of IDETC",
    "DFMLC": "Design for Manufacturing and Life Cycle Conference, part of IDETC",
    "DTM": "Design Theory and Methdology Conference, part of IDETC",
    "SEIKM": "Systems Engineering, Information, Knowledge Management Conference, part of CIE",
    "DCC": "Design Computing and Cognition",
    "DED": "Design Engineering Division, part of ASME",
    "ICED": "International Conference on Engineering Design",
    "SIG": "Special Interest Group",
}