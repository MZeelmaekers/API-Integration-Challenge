# API Assignment - Spotify - Zeelmaekers Maxim - R0781323
#import require modules
import base64
import requests
user_id = "7712521c15294edf864724788e6724d3"
user_secret = "c5eba5c0adf642e6a7bc03ae0164b514"

method= "POST"
token_url = "https://accounts.spotify.com/api/token"

#Encoding credentials to base64 needed for spotify
#Encoding first to bytes then converting bytes to base 64
#use decode else you get byets mixed in with your base64
user_creds = f"{user_id}:{user_secret}"
user_creds64 = base64.b64encode(user_creds.encode())
user_creds64 = user_creds64.decode()
print(user_creds64)

token_data = {
    "grant_type: user_credentials"
}

token_header = {

    "Authorization": f"Basic {user_creds64.decode()}"
}
r = requests.post(token_url, data=token_data, headers=token_header)
print(r.json())
