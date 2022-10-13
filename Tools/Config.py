import json


class Config:
    text: json
    commands: json
    buttons: json

    def __init__(self, config: json):
        self.text = config["text"][0]
        self.commands = config["commands"][0]
        self.buttons = config["buttons"][0]
