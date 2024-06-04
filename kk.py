import random
import json


def random_card():
    card_number = ""
    ccv = random.randrange(100,999)
    is_valid = True
    title = "Test Card"

    for i in range(16):
        number = str(random.randint(0,9))
        card_number += number
    censored_number = card_number[:4]+"********"+card_number[-4:]

    data = {
        "censored_card": censored_number,
        "ccv": ccv,
        "is_valid": is_valid,
        "title": title
    }

    json_data = json.dumps(data,indent=4)
    return json_data



random_card()