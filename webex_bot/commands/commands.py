import logging
import random
import time

from webex_bot.formatting import quote_info, quote_warning
from webex_bot.models.command import Command

log = logging.getLogger(__name__)
team_members = []
team_statuses = {}

with open('team_members.txt') as file:
    for member in file:
        team_members.append(member)
        team_statuses[member] = True
    random.shuffle(team_members)

class AssignCommand(Command):
    def __init__(self):
        super().__init__(command_keyword='!assign',
                         help_message='')

    def execute(self, message, attachment_actions, activity):
        for team_member in team_members:
            if team_statuses[team_member]:
                team_statuses[team_member] = False
                team_members.remove(team_member)
                team_members.append(team_member)
                return f"\nCase assigned to {team_member} \n"

class ReturnCommand(Command):
    def __init__(self):
        super().__init__(command_keyword='!return',
                         help_message='Return who was recently unavalible')

    def execute(self, team_member, attachment_actions, activity):
        if team_member in team_statuses:
            team_statuses[team_member] = True
            return f"\n{team_member} is now marked as available.\n"
        else:
            return f"\n{team_member} is not a valid team member.\n"

class SkipCommand(Command):
    def __init__(self):
        super().__init__(command_keyword='!skip',
                         help_message='Skips who is up next')

    def execute(self, message, attachment_actions, activity):
        team_member = team_members.pop(0)
        team_statuses[team_member] = False
        team_members.append(team_member)
        return f"\nSkipped {team_member}. They are now marked as unavailable.\n"
      
class FloaterCommand(Command):
    def __init__(self):
        super().__init__(command_keyword="!floaters",
                         help_message="display floaters")

    def execute(self, message, attachment_actions, activity):
        retString = [
        "## Up next:",
        quote_warning(team_members[0]),
        "## Rest of the team members: ",
        quote_info("".join(team_members[1:]))
        ]
        
        return retString