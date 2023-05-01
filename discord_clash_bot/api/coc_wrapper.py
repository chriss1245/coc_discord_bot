import requests
from discord_clash_bot.db.schema import Member, Clan

class CocClient():
    """
    Clash of Clans API wrapper
    """
    
    def __init__(self, token):
        self.token = token
        self.prefix = "https://api.clashofclans.com/v1/"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_clan(self, clan_tag):
        """
        Returns clan information
        """
        url = f"{self.prefix}clans/{clan_tag.replace('#', '%23')}"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_war(self):
        """
        Returns current clan war information
        """
        url = f"{self.prefix}clans/{clan_tag.replace('#', '%23')}/currentwar"
        r = requests.get(url, headers=self.headers)
        return r.json()
    
    def get_player(self, player_tag):
        """
        Returns player information
        """
        url = f"{self.prefix}players/%23{player_tag.strip('#')}"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_clan_members(self, clan_tag):
        """
        Returns clan members
        """
        members = self.get_clan(clan_tag).get("memberList")

        # create a list of players
        players = []
        
        for member in members:
            players.append(Member(member["name"],
                            member["tag"],
                            clan_tag,
                            member["role"],
                            member.get("warPreference"))
            )
        return players