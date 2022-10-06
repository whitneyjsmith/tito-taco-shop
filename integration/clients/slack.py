from slack_sdk import WebClient
from slack_sdk.rtm_v2 import RTMClient
from integration.models import TeamUser, Team
from ledger.models import TacoLedger
from django.conf import settings
from django.db.models import Sum
from datetime import datetime
import functools
import re

emoji = ":test"

class Client():
    def __init__(self, team_id, team_name, bot_token):
        self.team_id = team_id
        self.team_name = team_name
        self.client = None
        self.rtm_client = RTMClient(token=bot_token)

    def get_users(self, exclude_bots=True, include_deleted=False):
        res = self.client.users_list()
        users = res['members']
        if not exclude_bots and include_deleted:
            return users
        elif not exclude_bots and not include_deleted:
            return [user for user in res['members'] if not user['deleted']]
        return [user for user in res['members'] if not user['is_bot']
                and not user['deleted']]

    def log_users(self, users=None):
        if not users:
            users = self.get_users()
        team = Team.objects.get(team_id=self.team_id)
        for user in users:
            if not user['profile'].get('email'):
                continue
            TeamUser.objects\
                .update_or_create(team=team,
                                  user_team_id=user['id'],
                                  defaults={"email": user['profile']['email'],
                                            "details": user})

    def award_message(self, sender, receiver, amount):
        self.client.web_client.chat_postMessage(
            channel=receiver,
            as_user=True,
            text=f"Congratulations! You have received {amount} " +
            f"taco{'s' if amount > 1 else ''} from " +
            f"<@{sender}>!"
        )

    def confirmation_message(self, sender, receiver, amount, remaining):
        self.client.web_client.chat_postMessage(
            channel=sender,
            as_user=True,
            text=f"You have sent {amount} " +
            f"taco{'s' if amount > 1 else ''} to " +
            f"<@{receiver}>! You have {remaining} " +
            f"taco{'s' if remaining > 1 else ''} remaining to give today."
        )

    def overdraft(self, sender, recipients, remaining, amount):
        self.client.web_client.chat_postMessage(
            channel=sender,
            as_user=True,
            text=f"I regret to inform you that your taco transaction of " +
            f"{amount} taco{'s' if amount > 1 else ''} to " +
            ", ".join([f"<@{i}>" for i in recipients]) +
            f" is impossible as you have {remaining} left to give today, " +
            "and the bank of Tito does not have good overdraft fees. " +
            "Please try again."
        )

    def award_taco(self, message, sender, send_alert=True):
        print("Award Taco Called")
        recipients = re.findall(r'<@([^>]*)>', message)
        print(f"Recipients: {recipients}")
        # Remove self-given tacos
        while sender in recipients:
            recipients.remove(sender)
        print("Checking for multi tacos")
        multi_tacos = re.findall(r"(?<=test)(\d+)(?=:)", message)
        num_tacos = message.count(f'{emoji}:') + sum(map(int, multi_tacos))
        print(f"Num tacos: {num_tacos}")
        given_today = TacoLedger.objects.filter(
            giver=sender,
            timestamp__date=datetime.date(datetime.now())
        ).aggregate(Sum('amount')).get('amount__sum', 0) or 0
        print(f"Given today: {given_today}")
        tacos_remaining = (settings.TACO_DAILY_CAP -
                           (given_today + (num_tacos * len(recipients))))
        if tacos_remaining >= 0:
            print("SENDING RECEIPT")
            for recipient in set(recipients):
                ledger = TacoLedger.objects.create(
                    receiver=recipient,
                    giver=sender,
                    amount=num_tacos
                )
                self.award_message(sender, recipient, num_tacos)
                self.confirmation_message(sender, recipient,
                                          num_tacos, tacos_remaining)
        else:
            print("SENDING OVERDRAFT")
            self.overdraft(sender, recipients, tacos_remaining, num_tacos)

    def listen(self, client, event):
        if not self.client:
            self.client = client
        print(event)
        text = event.get('text', '')
        sender = event.get('user', '')
        if emoji in text and '<@' in text:
            print("EMOJI AND TAG DETECTED")
            print(text.count(emoji))
            if text.count(emoji) == 1:
                print("SENDING SINGLE TACO")
                self.award_taco(text, sender)
            else:
                print("SENDING MULTIPLE TACO")
                # Split on newlines so we don't double award
                for message in text.split('\n'):
                    self.award_taco(message, sender)

    def connect(self):
        print("Connecting to Slack RTM")
        self.rtm_client.on("message")(functools.partial(self.listen.__func__,
                                                        self))
        self.rtm_client.start()
