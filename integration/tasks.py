from slack_sdk import WebClient
from .models import TeamUser, Team
from django.contrib.auth import get_user_model
User = get_user_model()


class Slack():
    def __init__(self, team_id, team_name, bot_token):
        self.team_id = team_id
        self.team_name = team_name
        self.client = WebClient(token=bot_token)

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
            TeamUser.objects.update_or_create(team=team,
                                              user_team_id=user['id'],
                                              defaults={"email": user['profile']['email'],
                                                        "details": user})
