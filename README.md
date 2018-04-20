Data Sources Used:
FoodNetwork.com/profiles/talent (No Authorization required)
  - all of the chef's personal pages and recipe pages were also scraped
Spotify Web API (Client_Id and Client_Secret Needed) - a secrets.py file and a .gitignore for it is needed
(https://beta.developer.spotify.com/documentation/web-api/)
Plotly:
https://plot.ly/python/

Structure:
The interactive system is through the function interactive_prompt which then leads users
through a series of other functions such as chef() and dish() which then process the
user's command through process_chef() etc and make requests to the DB.

There is a large list at the beginning of the program that categorizes chefs
and flavor profiles. This was manually created based on info from FoodNetwork, but
could not be scraped directly because the information is not available in categorical terms.

User Guide:
Run the interactive_prompt. The messages onscreen will direct you clearly to the different
options you have. When there is an option for a plotly graph, the screen will tell you.
The program is made to take you through dishes first and then through to music in a pretty linear
manner. 
