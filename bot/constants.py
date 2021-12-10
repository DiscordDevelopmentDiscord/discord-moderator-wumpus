from discord_slash.utils.manage_commands import create_choice
from calendar import monthrange

GUILDS_PRONOUN_ROLES = {
    # Discord Developer Discord
    844686108125429801: {
        "he-him": 846008528174579742,
        "she-her": 846008548563091486,
        "they-them": 846008568620122182,
        "she-they": 918925357158121552,
        "he-they": 918925320311148644,
        "any": 846008593802461204,
        "ask": 846008616758018088,
    },
    # Discord Moderator Discord
    667560445975986187: {
        "he-him": 740020232315207770,
        "she-her": 740020247192404008,
        "they-them": 740020260521902193,
        "she-they": 918923092502388807,
        "he-they": 918923159019880458,
        "any": 834100284597862456,
        "ask": 834156042283253760,
    },
    # Moderator Mentorship Community
    813988123260092416: {
        "he-him": 813988123260092421,
        "she-her": 813988123260092420,
        "they-them": 813988123260092419,
        "she-they": 918924844756795402,
        "he-they": 918924912134082651,
        "ask": 846009253332254730,
        "any": 846009307627520011,
    },
}

PRONOUN_OPTIONS = [
    create_choice(
        value="he-him",
        name="He/Him",
    ),
    create_choice(
        value="she-her",
        name="She/Her",
    ),
    create_choice(
        value="they-them",
        name="They/Them",
    ),
    create_choice(
        value="she-they",
        name="She/They",
    ),
    create_choice(
        value="he-they",
        name="He/They",
    ),
    create_choice(
        value="any",
        name="Any Pronouns",
    ),
    create_choice(
        value="ask",
        name="Ask for Pronouns",
    ),
]

DMA_API_URL = "https://discordmoderatoracademy.zendesk.com/api/v2/help_center/en-us/articles"
DMA_API_SEARCH_URL = (
    "https://discordmoderatoracademy.zendesk.com/api/v2/help_center/articles/search"
)

DMA_TITLE_REGEX = r"^\d\d\d:\s.*$"
DMA_QUERY_REGEX = r"[{}]"
DMA_SERIES_NAMES = {
    1: "Basics",
    2: "Setup and Function",
    3: "Advanced Community Management",
    4: "Moderation Seminars",
    5: "Graduate Classes",
}
DMA_SERIES_IDS = {
    1: "360011920213",
    2: "360010792534",
    3: "360011920293",
    4: "360011920313",
    5: "4405269416471",
}
DMA_CATEGORY_NAMES = {
    0: "Foundational Understanding",
    1: "Human Moderation",
    2: "Bots and Automation",
    3: "Community Management and Growth",
    4: "Advanced Topics",
    5: "External Services",
}

AUTOROLE_CONFIG = {
    813988123260092416: {
        "DISCORD": 813988123260092422,
        "MODERATOR": 813988123260092423,
        "MEMBER": 813988123260092422,
    },
    667560445975986187: {
        "DISCORD": 687070754671558718,
        "MODERATOR": 808643136771457044,
        "MEMBER": 687070754671558718,
    },
}


def get_days(year: int, month: int):
    return monthrange(year, month)[1]


TIMESTAMP_MAKE_BOUNDARIES = [
    {"name": "year", "min": 1, "max": 9998},
    {"name": "month", "min": 1, "max": 12},
    {"name": "day", "min": 1, "max": get_days},
    {"name": "hour", "min": 0, "max": 23},
    {"name": "minute", "min": 0, "max": 59},
    {"name": "utc", "min": -12, "max": 14},
]
TIMESTAMP_RELATIVE_BOUNDARIES = [
    {"name": "days", "range": 730500},  # +- 2000 years, keeping well between 1 and 9999 for year
    {"name": "hours", "range": 23},
    {"name": "minutes", "range": 59},
]

SAFETY_API_ENDPOINT = "https://discordsafetyportal.zendesk.com/api/v2/help_center/articles/search"
SAFETY_IDS = [
    360043857751,  # Four steps to a super safe account
    360043653152,  # Four steps to a super safe server
    360044103531,  # Role of administrators and moderators on Discord
    360044103651,  # Reporting problems to Discord
    360044103771,  # Mental health on Discord
    360043653552,  # Adult content on Discord
    360044104071,  # Tips against spam and hacking
    360044149331,  # What is Discord?
    360043700632,  # Discord's commitment to a safe and trusted experience
    360044153831,  # Helping your teen stay safe on Discord
    360044154611,  # Talking about online safety with your teen
    360044149591,  # Answering parents' and educators' top questions
    360044154771,  # If your teen encounters an issue
    360057166133,  # Working with CARU to protect users on Discord
    360043709612,  # Our policies
    360044158971,  # Enforcing our rules
    360043712132,  # How we investigate
    360044159011,  # What actions we take
    360043712172,  # How you can appeal our actions
    360043712232,  # Discord's Transparency Report
    360044157931,  # Working with law enforcement
]  # ID's in order found on https://discord.com/safety from left to right categories, top to bottom.
SAFETY_CATEGORY_NAMES = {
    360009069551: "Controlling Your Experience",
    360009069571: "Parents & Educators",
    360008956792: "How We Enforce Rules",
}

BOT_DEVS = [165023948638126080, 141288766760288256, 249287049482338305]
