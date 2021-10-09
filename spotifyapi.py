# API Assignment - Spotify - Zeelmaekers Maxim - R0781323
# import require modules
import base64
from prettytable import PrettyTable
import requests

# Predeclared variabled | some may be empty to use later.
# API URL
url = "https://accounts.spotify.com/api/token"
i = 1

# Layout
line = "---------------------------------------------------------------------"
head = "API Assignment - Spotify - Zeelmaekers Maxim - R0781323 \n" +line +"  \nPlease follow the instructins below | Type exit to quit."
clear = "\n" * 100

# API Veriables | Will be used later!
headers = {}
data = {}
artist = ""

# Table decleration 
# X = Artist table
# Y = Top 10 tracks 
x = PrettyTable()
y = PrettyTable()


# ====================
# ---- Main code -----
# ====================
try:
    # Login menu - API Client ID & Secret
    # using exit to leave the prompt
    print(head)
    client_id = input("Please enter your API Client ID: ")
    print(clear)
    if client_id == "exit":
        quit()
    print(head)
    print("API Client ID accepted. ✓" )
    client_secret = input("Please enter your API client Secret: ")
    print(clear)
    if client_secret == "exit":
       quit()
    #check is client_id AND client_secret are give, if not ask again
    if client_secret == "" or client_id == "":
        print("please authenticate before continuing.")   
    

    # Encode to base64 as required by spotify API
    # See Authorization: Base 64 encoded string that contains the client ID and client secret key.
    # source: https://developer.spotify.com/documentation/general/guides/authorization-guide/
    client_creds = f"{client_id}:{client_secret}"
    client_creds64 = base64.b64encode(client_creds.encode())
    client_creds64 = client_creds64.decode()
    
    # Troubelshooting step to print base64 credentials. Uncomment line below
    # print("Base64 key = "+ client_creds64)

    # Setting up headers & variables needed for request
    headers['Authorization'] = f"Basic {client_creds64}"
    data['grant_type'] = "client_credentials"

    # Request API data with POST request
    tokendata = requests.post(url, headers=headers, data=data)
        
    # Check if API request was successvol (code 200)
    # see Response Status Codes
    # https://developer.spotify.com/documentation/web-api/
    if tokendata.status_code not in range(200, 299):
        print( "ERROR! \nWe were not able to authenicate you, please check your credentials.\n" + line + "\n"+"Your credentials were:" + "\nClient ID:"+ client_id + "\nClient Secret:"+ client_secret +"\n"+ line + "\nError Code: " + str(tokendata.status_code))
    
    else:
        
        access_token = tokendata.json()['access_token']
        # Troubelshooting step to print base64 credentials. Uncomment line below
        # print("Token = "+ token)

        print("\n" + head)
        artist = input("Please enter the name of the artist: ")
        if artist == "exit":
                quit()
        
        # Spotify_API_URL search for Artist with the artist variable.
        # see https://developer.spotify.com/console/get-search-item/
        # Set headers with API URL and Auth token. 
        # request the response in a JSON format with GET.
        Spotify_API_URL = f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1&market=BE"
        headers = {
            "Authorization": "Bearer " + access_token
        }
        request_json = requests.get(url=Spotify_API_URL, headers=headers).json()
        
        if request_json["artists"]["total"] == 0:
                print("Cannot find any artist with the name '" + artist + "' Check for spelling errors and try again.")
                
        # Troubleshooting step -> Print JSON file of the artist
        # Uncomment the line below
        # print(request_json)

        # Prepare API Calls and clear terminal
        # Documentation can be found https://developer.spotify.com/console/get-search-item/
        print(clear)

        #link artist id to json information.
        artist_ID = request_json["artists"]["items"][0]["id"]
        artist_Url = f"https://api.spotify.com/v1/artists/{artist_ID}"
        track_Url = f"https://api.spotify.com/v1/artists/{artist_ID}/top-tracks?market=BE"

        # Make API calls with get requests
        Artist = requests.get(url=artist_Url, headers=headers).json()
        Top10_Tracks = requests.get(url=track_Url, headers=headers).json()


        # Fill Table Y with Artist information
        x.field_names = ["Main", "Answer"]
        x.add_rows(
        [
            ["Name: ", Artist["name"]],
            ["Number of followers:", str(Artist["followers"]["total"])],
            ["Popularity",str(Artist["popularity"])],
            ["Genres", str(Artist["genres"])]
        ]
        )

        # Fill Table Y with Top 10 Tracks
        y.field_names = ["Number", "Track"]
        for track in Top10_Tracks["tracks"]:
            
            y.add_rows(
            [
            [str(i), track["name"]]
            ] 
            )
            i = i+1

        # Print tables
        # Table X = Artist infomrmation
        # Table Y = Top 10 Tracks
        print("Information about " + Artist["name"] + ":")
        print(x)
        print("Top 10 Tracks of " + Artist["name"] + ":")
        print(y)

#Error code catching
except Exception as e: print(e)
