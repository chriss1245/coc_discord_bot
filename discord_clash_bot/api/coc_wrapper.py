import requests
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