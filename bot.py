# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the pythOnBoarding app
"""
import io
import os
import message

import report

from slackclient import SlackClient

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistant memory store.
authed_teams = {}


class Bot(object):
    """ Instanciates a Bot object to handle Slack onboarding interactions."""
    def __init__(self, name, emoji):
        super(Bot, self).__init__()
        self.name = name
        self.emoji = emoji
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")

        # NOTE: Python-slack requires a client connection to generate
        # an oauth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = SlackClient("")
        # We'll use this dictionary to store the state of each message object.
        # In a production envrionment you'll likely want to store this more
        # persistantly in  a database.
        self.messages = {}

    def auth(self, code):
        """
        Authenticate with OAuth and assign correct scopes.
        Save a dictionary of authed team information in memory on the bot
        object.

        Parameters
        ----------
        code : str
            temporary authorization code sent by Slack to be exchanged for an
            OAuth token

        """
        # After the user has authorized this app for use in their Slack team,
        # Slack returns a temporary authorization code that we'll exchange for
        # an OAuth token using the oauth.access endpoint
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )
        # To keep track of authorized teams and their associated OAuth tokens,
        # we will save the team ID and bot tokens to the global
        # authed_teams object
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        # Then we'll reconnect to the Slack Client with the correct team's
        # bot token
        self.client = SlackClient(authed_teams[team_id]["bot_token"])

    def upload_file(self, file, channel, title):
        """
        Uploads a file as the method name suggests
        """
        client = SlackClient(os.environ.get("BOT_TOKEN"))

        client.api_call(
            'files.upload',
            channels=channel,
            file=file,
            title=title
        )


    def pleats_response(self, slack_event):
        client = SlackClient(os.environ.get("BOT_TOKEN"))

        if 'pleats' in slack_event['event']['text']:
            client.api_call(
                'chat.postMessage',
                channel=slack_event['event']['channel'],
                text='he is ok',
                username=self.name,
                icon_emoji=self.emoji
            )
        elif 'help' in slack_event['event']['text']:
            client.api_call(
                    'chat.postEphemeral',
                    channel=slack_event['event']['channel'],
                    text='Hello there, my name is ReportBot :wave:\nType `/transsum [branch] [client] [start_date] [end_date] [product]` to submit a report right away\nOr simply type `/transsum` for a report submission dialogue prompt',
                    user=slack_event['event']['user'],
                    username=self.name,
                    icon_emoji=self.emoji
            )
        elif 'morning' in slack_event['event']['text']:
            client.api_call(
                'chat.postMessage',
                channel=slack_event['event']['channel'],
                text='There he is!',
                username=self.name,
                icon_emoji=self.emoji
            )
        else:
            client.api_call(
                'chat.postMessage',
                channel='scrumlords',
                text='Hello!  I did not understand that',
                username=self.name,
                icon_emoji=self.emoji
            )

    def upload_report(self, channel, title, start_date, end_date, branch, client, name):
        """
        Generates a report and uploads it
        """
        generated_report = report.get_report(
            start_date,
            end_date,
            branch,
            client,
            name
        )

        with io.StringIO(generated_report) as file:
            self.upload_file(file, channel, title)

    def dialog_test(self, trigger_id, user_id):
        client = SlackClient(os.environ.get("BOT_TOKEN"))
        open_dialog = client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog={
                "title": "Test",
                "submit_label": "Press",
                "callback_id": "dialog-test",
                "elements": [
                    {
                        "label": "Branch",
                        "type": "text",
                        "name": "branch_no",
                    },
                    {
                        "label": "Client",
                        "type": "text",
                        "name": "client_no",
                    },
                    {
                        "label": "Start Date",
                        "type": "text",
                        "name": "start_date",
                    },
                    {
                        "label": "End Date",
                        "type": "text",
                        "name": "end_date",
                    },
                    {
                        "label": "Product",
                        "type": "select",
                        "name": "product",
                        "placeholder": "Select a product",
                        "options": [
                            {
                                "label": "DDS",
                                "value": "dds"
                            },
                            {
                                "label": "RCX",
                                "value": "rcx"
                            },
                            {
                                "label": "Both",
                                "value": "ddsrcx"
                            }
                        ]
                    }
                ]
            }
        )
        print(open_dialog)
