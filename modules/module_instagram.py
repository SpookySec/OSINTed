import requests

class Instagram:
    def __init__(self, username): 
        link = "https://www.instagram.com/"+username+"/?__a=1"
        self.parsed = requests.get(link).json()

    def username(self):
        return str(self.parsed["graphql"]["user"]["username"])

    def user_id(self):
        return str(self.parsed["graphql"]["user"]["id"])
    
    def fullname(self):
        return str(self.parsed["graphql"]["user"]["full_name"])
    
    def followers(self):
        return str(self.parsed["graphql"]["user"]["edge_followed_by"]["count"])

    def following(self):
        return str(self.parsed["graphql"]["user"]["edge_follow"]["count"])

    def profile_pic(self):
        return str(self.parsed["graphql"]["user"]["profile_pic_url_hd"])

    def bio(self):
        return str(self.parsed["graphql"]["user"]["biography"])

    def posts(self):
        return str(self.parsed["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])
    
    def url(self):
        return str(self.parsed["graphql"]["user"]["external_url"])
    
    def business(self):
        return str(self.parsed["graphql"]["user"]["is_business_account"])
    
    def recently(self):
        return str(self.parsed["graphql"]["user"]["is_joined_recently"])

    def private(self):
        return str(self.parsed["graphql"]["user"]["is_private"])

    def verified(self):
        return str(self.parsed["graphql"]["user"]["is_verified"])

    def business_category(self):
        return str(self.parsed["graphql"]["user"]["business_category_name"])

    def isValid(self):
        try:
            str(self.parsed["graphql"]["user"]["username"])
            return True
        except KeyError:
            return False
