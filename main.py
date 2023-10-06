import functions_framework

from typing import Any, Mapping

import flask
import functions_framework

# Google Cloud Function that responds to messages sent in
# Google Chat.
#
# @param {Object} req Request sent from Google Chat.
# @param {Object} res Response to send back.
@functions_framework.http
def hello_chat(req: flask.Request):
    if req.method == "GET":
        return "Hello! This function must be called from Google Chat."

    request_json = req.get_json(silent=True)

    display_name = request_json["message"]["sender"]["displayName"]
    avatar = request_json["message"]["sender"]["avatarUrl"]

    response = create_message(name=display_name, image_url=avatar)

    return response


# Creates a card with two widgets.
# @param {string} name the sender's display name.
# @param {string} image_url the URL for the sender's avatar.
# @return {Object} a card with the user's avatar.
def create_message(name: str, image_url: str) -> Mapping[str, Any]:
    avatar_image_widget = {"image": {"imageUrl": image_url}}
    avatar_text_widget = {"textParagraph": {"text": "Your avatar picture:"}}
    avatar_section = {"widgets": [avatar_text_widget, avatar_image_widget]}

    header = {"title": f"Hello {name}!"}

    cards = {
        "cardsV2": [
            {
                "cardId": "avatarCard",
                "card": {
                    "name": "Avatar Card",
                    "header": header,
                    "sections": [avatar_section],
                },
            }
        ]
    }

    return cards
