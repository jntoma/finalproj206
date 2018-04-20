import requests
from bs4 import BeautifulSoup
import json
import secrets
from requests_oauthlib import OAuth1
from operator import itemgetter
import sqlite3
import csv
import base64
import itertools
import plotly.plotly as py
import plotly.graph_objs as go
import webbrowser

spotifybase = "https://accounts.spotify.com/api/token"
spotifyplay = "https://api.spotify.com/v1/search"
foodnet = "https://www.foodnetwork.com/profiles/talent"

spotify_client = secrets.client_id
spotify_secret = secrets.client_secret
auth = (spotify_client, spotify_secret)
grant_type = 'client_credentials'

CACHE_FNAME = 'final_cache.json'
DBNAME = 'food.db'
CHEFS = 'chefs.json'
DISHES = 'dishes.json'

flavor_dict = {'Aaron McCargo Jr.': 'American',
'Aarti Sequeira': 'South Asian',
'Aarón Sánchez': 'Latin',
'Adam Gertler': 'BBQ',
'Aida Mollenkamp': 'Innovative',
'Alex Guarnaschelli': 'Traditional Home-Cooking',
'Amanda Freitag': 'Traditional Home-Cooking',
'Amy Thielen': 'Traditional Home-Cooking',
'Andrew Zimmern': 'Innovative',
'Anne Burrell': 'Rustic',
'Anne Thornton': 'Sweet Treats',
'Ayesha Curry': 'Home-Cooking',
'Bob Blumer': 'Innovative',
'Bobby Flay': 'American',
'Brian Boitano': 'Innovative',
'Buddy Valastro': 'Sweet Treats',
'Carla Hall': 'Southern Comfort',
'Cat Cora': 'Misc.',
'Chris Santos': 'Innovative',
'Claire Robinson': 'Home-Cooking',
'Curtis Stone': 'Home-Cooking',
'Daisy Martinez': 'Latin',
'Damaris Phillips': 'Southern Comfort',
'Danny Boome': 'Healthy',
'Daphne Brogdon': 'Home-Cooking',
'Dave Lieberman': 'Home-Cooking',
'Donatella Arpaia': 'Home-Cooking',
'Duff Goldman': 'Sweet Treats',
'Eddie Jackson': 'Healthy',
'Ellie Krieger': 'Healthy',
'Emeril Lagasse': 'Misc.',
'Food Network Kitchen': 'Misc.',
'Geoffrey Zakarian': 'Modern American',
'George Duran': 'Global Cuisine',
'Giada De Laurentiis': 'Italian',
'Graham Elliot': 'Misc.',
'Guy Fieri': 'American',
'Ina Garten': 'Home-Cooking',
'Ingrid Hoffmann': 'Misc.',
'Jamie Deen': 'BBQ',
'Jamie Oliver': 'Healthy',
'Janet Johnston': 'Home-Cooked',
'Jeff Corwin': 'Latin',
'Jeff Mauro': 'Misc.',
'Jet Tila': 'East Asian',
'Joey Fatone': 'American',
'Jose Garces': 'Latin',
'Judy Joo': 'Misc.',
'Katie Lee': 'Misc.',
'Keegan Gerhard': 'Sweet Treats',
'Kerry Vincent': 'Sweet Treats',
'Lorraine Pascale': 'Home-Cooking',
'Maneet Chauhan': 'South Asian',
'Marc Murphy': 'Modern American',
'Marcela Valladolid': 'Latin',
'Marcus Samuelsson': 'Misc.',
'Mario Batali': 'Italian',
'Mary Nolan': 'Everyday',
'Masaharu Morimoto': 'East Asian',
"Melissa d'Arabian": 'Healthy',
'Michael Chiarello': 'Italian',
'Michael Symon': 'Misc.',
'Nancy Fuller': 'Southern Comfort',
'Nigella Lawson': 'Home-Cooking',
'Patricia Heaton': 'American',
'Paula Deen': 'Southern',
'Rachael Ray': 'Everyday',
'Ree Drummond': 'Southern Comfort',
'Robert Irvine': 'American',
'Robin Miller': 'Everyday',
'Roger Mooking': 'Global Cuisine',
'Ron Ben-Israel': 'Sweet Treats',
'Sandra Lee': 'American',
'Scott Conant': 'Italian',
'Sherry Yard': 'Sweet Treats',
'Sunny Anderson': 'Southern Comfort',
'Ted Allen': 'American',
'The Hearty Boys': 'Innovative',
'The Neelys': 'BBQ',
'Tia Mowry': 'Everyday',
'Tregaye Fraser': 'Innovative',
'Trisha Yearwood': 'Southern Comfort',
'Tyler Florence': 'Home-Cooking',
'Valerie Bertinelli': 'Misc.',
'Warren Brown': 'Sweet Treats'}

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

try:
    cache_file = open(CHEFS, 'r')
    cache_contents = cache_file.read()
    CHEF_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CHEF_DICTION = {}

try:
    cache_file = open(DISHES, 'r')
    cache_contents = cache_file.read()
    DISH_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    DISH_DICTION = {}

def get_spotify_token(url, auth):
    params = {'grant_type': grant_type}
    # if url in CACHE_DICTION:
    #     access_token = CACHE_DICTION[url][17:100]
    #     return access_token
    # else:
    resp = requests.post(url, data=params, auth=auth)
    resp_data = json.loads(resp.text)
    access_token = resp_data["access_token"]
    CACHE_DICTION[url] = resp.text
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close()
    return access_token

def make_request_using_cache(url, headers=None):
    if url in CACHE_DICTION:
        return CACHE_DICTION[url]
    else:
        if headers is None:
            resp = requests.get(url)
        else:
            resp = requests.get(url, headers=headers)
        CACHE_DICTION[url] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[url]

def get_spotify_playlist(search_term):
    end = ["party", "graph", "term"]
    params = {'q': search_term}
    url = "{}?type=playlist&limit=5&q=".format(spotifyplay) + search_term
    access_token = get_spotify_token(spotifybase, auth)
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    response_string = make_request_using_cache(url, authorization_header)
    response = json.loads(response_string)
    num = 0
    spotify_list = []
    for r in response:
        for i in range(5):
            num += 1
            spotify_list.append((response[r]["items"][i]["name"], str(response[r]["items"][i]["tracks"]["total"])))
            print(str(num) + ". " + response[r]["items"][i]["name"] + " --- " + str(response[r]["items"][i]["tracks"]["total"]))
    print("Do you want to see a bar graph comparing these playlist's lengths,"
    "look up another term, or"
    " do you want to go start throwing your awesome party?")
    response = input("Please enter 'party', 'term', or 'graph': ")
    while response not in end:
        response = input("Please enter 'party', 'term', or 'graph': ")
    if response == 'party':
        print("Bye! Have fun!")
        exit()
    elif response == 'graph':
        bar_graph_spotify(spotify_list)
        print("Alright! Time for you to go throw the best party out there! See you later!")
        exit()
    elif response == 'term':
        response = input("Please enter a new search term! ")
        get_spotify_playlist(response)
    return spotify_list


def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
            DROP TABLE IF EXISTS 'Chefs';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Dishes';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Chefs' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'FirstName' TEXT NOT NULL,
            'LastName' TEXT NOT NULL,
            'ChefUrl' TEXT NOT NULL,
            'PopularRecipe' TEXT,
            'FlavorProfile' TEXT
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Dishes' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'DishName' TEXT NOT NULL,
                'DishUrl' TEXT NOT NULL,
                'ChefID' INTEGER,
                'Type' TEXT NOT NULL,
                'LevelDifficulty' TEXT NOT NULL,
                'Rating' INTEGER
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

class Chef:
    def __init__(self, FirstName, LastName, ChefUrl=None):
        self.FirstName = FirstName
        self.LastName = LastName
        self.ChefUrl = ChefUrl
        self.full_name = FirstName + " " + LastName

        if ChefUrl is not None:
            unique_page_text = make_request_using_cache(ChefUrl)
            unique_page_soup = BeautifulSoup(unique_page_text, 'html.parser')

            if self.full_name in flavor_dict:
                try:
                    most_popular_block = unique_page_soup.find(class_ = "m-MediaBlock o-Capsule__m-MediaBlock m-MediaBlock--recipe")
                    most_popular = most_popular_block.find(class_="m-MediaBlock__a-HeadlineText").text
                    self.FlavorProfile = flavor_dict[self.full_name]
                    if self.full_name == "Bobby Flay" or self.full_name == "Duff Goldman" or self.full_name == "Melissa D'Arabian" or self.full_name == "Nigella Lawson":
                        recipes_url = ChefUrl + "/recipes"
                        recipes_text = make_request_using_cache(recipes_url)
                        recipes_soup = BeautifulSoup(recipes_text, 'html.parser')
                        recipes_list = recipes_soup.find(class_ = "l-List")
                        most_popular = recipes_list.find(class_ = "m-MediaBlock__a-HeadlineText").text
                except:
                    most_popular = "N/A"
            else:
                most_popular = "N/A"
                self.FlavorProfile = "N/A"

            self.PopularRecipe = most_popular
        else:
            self.PopularRecipe = "N/A"

class Dish:
    def __init__(self, DishName, DishUrl, Rating, Chef):
        dish_types = ["Side Dish", "Main Dish", "Snack Dish", "Dessert"]
        self.DishName = DishName
        self.DishUrl = "http:" + DishUrl
        self.Rating = Rating
        self.Chef = Chef
        dish_type = "Unknown"
        dish_page_text = make_request_using_cache(self.DishUrl)
        dish_page_soup = BeautifulSoup(dish_page_text, 'html.parser')
        try:
            level_all = dish_page_soup.find(class_ = "o-RecipeInfo o-Level")
            level = level_all.find(class_ = "o-RecipeInfo__a-Description").text
        except:
            level = "Unknown"
        try:
            tags = dish_page_soup.find_all(class_ = "o-Capsule__a-Tag a-Tag")
            for t in tags:
                if t.text in dish_types:
                    dish_type = t.text
                else:
                    dish_type = "Unknown"
        except:
            dish_type = "Unknown"
            pass
        self.Type = dish_type
        self.LevelDifficulty = level
        pass

def get_chef_info():
    init_page_text = make_request_using_cache(foodnet)
    init_page_soup = BeautifulSoup(init_page_text, 'html.parser')
    name_list = init_page_soup.find_all(class_="m-PromoList__a-ListItem")
    chef_list = []
    num = 0
    for n in name_list:
        first_name = n.text.split(" ")[0]
        second_word = n.text.split(" ")[1]
        last_name = n.text.split(" ")[1:]
        if len(last_name) == 2:
            last_name = last_name[0] + " " + last_name [1]
        elif len(last_name) == 3:
            last_name = last_name[0] + " " + last_name [1] + " " + last_name [2]
        else:
            last_name = last_name[0]
        if second_word == "and":
            first_name = n.text.split(" ")[0] + " and " + n.text.split(" ")[2]
            last_name = n.text.split(" ")[3]
        chef_url = "https:" + n.find('a')['href']
        n = Chef(first_name, last_name, chef_url)
        chef_list.append(n)
        chef = {"FirstName": n.FirstName,
        "LastName": n.LastName,
        "ChefUrl": n.ChefUrl,
        "PopularRecipe": n.PopularRecipe,
        "FlavorProfile": n.FlavorProfile}
        CHEF_DICTION[n.full_name] = chef
    chef_string = json.dumps(CHEF_DICTION, indent = 4)
    fw = open(CHEFS,"w")
    fw.write(chef_string)
    fw.close()
    return chef_list

def get_dish_info():
    chefs = get_chef_info()
    dishes_list = []
    for c in chefs:
        chef_dishes = []
        if c.full_name in flavor_dict:
            dishes_url = c.ChefUrl + "/recipes"
            init_page_text = make_request_using_cache(dishes_url)
            init_page_soup = BeautifulSoup(init_page_text, 'html.parser')
            try:
                next_button = init_page_soup.find(class_ = "o-Pagination__a-Button o-Pagination__a-NextButton")
            except:
                next_button = "No"
            big_list = init_page_soup.find(class_="l-List")
            ratings_list = []
            try:
                dish_list = big_list.find_all(class_ = "m-MediaBlock__a-Headline")
            except:
                pass
            try:
                ratings = big_list.find_all(class_ = "gig-rating-stars")['title']
                for r in ratings:
                    print(r)
                ratings_list.append(ratings)
            except:
                ratings = "Unknown"
                ratings_list.append(ratings)
            try:
                for d in dish_list:
                    dish_name = d.text
                    dish_url = d.find('a')["href"]
                    dish_rating = "5 out of 5"
                    d = Dish(dish_name, dish_url, dish_rating, c.full_name)
                    dishes_list.append(d)
                    dish = {"DishName": d.DishName,
                    "DishUrl": d.DishUrl,
                    "DishRating": d.Rating,
                    "Type": d.Type,
                    "LevelDifficulty": d.LevelDifficulty}
                    chef_dishes.append(dish)
            except:
                pass
            # num = 1
            # while next_button != "No":
            #     num += 1
            #     next_url = dishes_url + "/trending-/p/" + str(num)
            #     next_page = make_request_using_cache(next_url)
            #     next_page_soup = BeautifulSoup(next_page, 'html.parser')
            #     try:
            #         next_button = init_page_soup.find(class_ = "o-Pagination__a-Button o-Pagination__a-NextButton")
            #     except:
            #         next_button = "No"
            #     big_list = next_page_soup.find(class_="l-List")
            #     ratings_list = []
            #     try:
            #           dish_list = big_list.find_all(class_ = "m-MediaBlock__a-Headline")
            #     except:
            #           dish_list = "no dishes"
            #     try:
            #           ratings = big_list.find_all(class_ = "gig-rating-stars")['title']
            #       for r in ratings:
            #           print(r)
            #       ratings_list.append(ratings)
            #     except:
            #         ratings = "Unknown"
            #         ratings_list.append(ratings)
            #     try:
            #         for d in dish_list:
            #             dish_name = d.text
            #             dish_url = d.find('a')["href"]
            #             dish_rating = ""
            #             d = Dish(dish_name, dish_url, dish_rating, c.full_name)
            #             dishes_list.append(d)
            #             dish = {"DishName": d.DishName,
            #             "DishUrl": d.DishUrl,
            #             "DishRating": d.Rating,
            #             "Type": d.Type,
            #             "LevelDifficulty": d.LevelDifficulty}
            #             chef_dishes.append(dish)
            #     except:
            #         pass
            #     if num == 2:
            #         break
            #     try:
            #         next_button = next_page_soup.find(class_ = "o-Pagination__a-Button o-Pagination__a-NextButton").text
            #     except:
            #         next_button = "No"
        DISH_DICTION[c.full_name] = chef_dishes
    dish_string = json.dumps(DISH_DICTION, indent = 4)
    fw = open(DISHES,"w")
    fw.write(dish_string)
    fw.close()
    #print(dishes_list[:30])
    return dishes_list

def insert_data():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)
    #
    # #print('Inserting Data.')
    with open(CHEFS) as json_data:
        cjson = json.load(json_data)
        for c, d in cjson.items():
            insertion = (None, d["FirstName"], d["LastName"], d["ChefUrl"], d["PopularRecipe"], d["FlavorProfile"])
            statement = 'INSERT INTO "Chefs" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)

    chef_dict = {}

    statement = '''SELECT Id, FirstName, LastName FROM Chefs'''
    cur.execute(statement)
    for chef_info in cur:
        full_name = chef_info[1] + " " + chef_info [2]
        chef_dict[full_name] = chef_info[0]


    with open(DISHES) as json_data:
        cjson = json.load(json_data)
        for c, d in cjson.items():
            full_name = c
            for i in d:
                insertion = (None, i["DishName"].replace("\n", ""), i["DishUrl"], chef_dict[full_name], i["Type"], i["LevelDifficulty"].replace("\n", ""), i["DishRating"])
                statement = 'INSERT INTO "Dishes" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def pie_chart(flavor_chef):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    labels = []
    values = []
    for f in flavor_chef:
        labels.append(f)
        first_name = f.split(" ")[0]
        second_word = f.split(" ")[1]
        last_name = f.split(" ")[1:]
        if len(last_name) == 2:
            last_name = last_name[0] + " " + last_name [1]
        elif len(last_name) == 3:
            last_name = last_name[0] + " " + last_name [1] + " " + last_name [2]
        else:
            last_name = last_name[0]
        if second_word == "and":
            first_name = f.split(" ")[0] + " and " + f.split(" ")[2]
            last_name = f.split(" ")[3]
        query = '''
        SELECT COUNT(*)
        FROM Chefs as c
        JOIN Dishes as d
        ON c.ID = d.ChefID
        WHERE c.FirstName = "{}" AND c.LastName = "{}"
        GROUP BY c.ID
        '''.format(first_name, last_name)
        value = cur.execute(query)
        for v in value:
            values.append(v[0])
    trace = go.Pie(labels=labels, values=values)

    py.plot([trace], filename='Flavors')

def bar_graph_spotify(spotify):
    x = []
    y = []
    for w, z in spotify:
        x.append(w)
        y.append(z)
    data = [go.Bar(
            x = x,
            y = y
    )]
    py.plot(data, filename='bar-Spotify')

def bar_graph_type(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    chef_types = {}
    first_name = command.split(" ")[0]
    second_word = command.split(" ")[1]
    last_name = command.split(" ")[1:]
    if len(last_name) == 2:
        last_name = last_name[0] + " " + last_name [1]
    elif len(last_name) == 3:
        last_name = last_name[0] + " " + last_name [1] + " " + last_name [2]
    else:
        last_name = last_name[0]
    if second_word == "and":
        first_name = command.split(" ")[0] + " and " + command.split(" ")[2]
        last_name = command.split(" ")[3]
    query = '''
    SELECT COUNT(*), d.Type
    FROM Chefs as c
    JOIN Dishes as d
    ON c.ID = d.ChefID
    WHERE c.FirstName = "{}" AND c.LastName = "{}"
    GROUP BY d.Type
    '''.format(first_name, last_name)
    types = cur.execute(query)
    x = []
    y = []
    for t in types:
        print(t)
        x.append(t[1])
        y.append(t[0])
    data = [go.Bar(
            x = x,
            y = y
    )]
    py.plot(data, filename='bar-Type')

def process_flavors(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    flavor_chef = []
    query = '''
    SELECT FirstName, LastName
    FROM Chefs
    WHERE FlavorProfile = "{}"
    '''.format(command)
    chefs = cur.execute(query)
    for c in chefs:
        full_name = c[0] + " " + c[1]
        flavor_chef.append(full_name)
    return flavor_chef
    conn.close()

def process_chef(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    dishes_o_chefs = []
    first_name = command.split(" ")[0]
    second_word = command.split(" ")[1]
    last_name = command.split(" ")[1:]
    if len(last_name) == 2:
        last_name = last_name[0] + " " + last_name [1]
    elif len(last_name) == 3:
        last_name = last_name[0] + " " + last_name [1] + " " + last_name [2]
    else:
        last_name = last_name[0]
    if second_word == "and":
        first_name = command.split(" ")[0] + " and " + command.split(" ")[2]
        last_name = command.split(" ")[3]
    query = '''
    SELECT d.DishName, d.DishUrl, d.Rating, d.Type, d.LevelDifficulty
    FROM Chefs as c
    JOIN Dishes as d
    ON c.ID = d.ChefID
    WHERE c.FirstName = "{}" AND c.LastName = "{}"
    '''.format(first_name, last_name)
    dishes = cur.execute(query)
    for d in dishes:
        dish = {}
        formatted = d[0] + "--- " + d[3] + ", " + d[2] + ", Level: " + d[4]
        dish[d[0]] = [d[1], d[2], d[3], d[4]]
        dishes_o_chefs.append(dish)
    conn.close()
    return dishes_o_chefs

def process_dish(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    dish = []
    query = '''
    SELECT d.DishName, d.DishUrl, d.Rating, d.Type, d.LevelDifficulty
    FROM Chefs as c
    JOIN Dishes as d
    ON c.ID = d.ChefID
    WHERE d.Type = "{}"
    LIMIT 1
    '''.format(command)
    dishes = cur.execute(query)
    for d in dishes:
        one_dish = {}
        formatted = d[0] + "--- " + d[3] + ", " + d[2] + ", Level: " + d[4]
        one_dish[d[0]] = [d[1], d[2], d[3], d[4]]
        dish.append(one_dish)
    conn.close()
    return dish

def flavors():
    flavors = ["American", "BBQ", "East Asian", "Everyday", "Global Cuisine", "Healthy",
    "Home-Cooking","Innovative","Italian","Latin","Misc.","Modern American",
    "Rustic","Southern Comfort","South Asian","Sweet Treats","Trad. Home-Cooking", "exit"]
    one_two = ["1", "2", "exit"]

    print("Here are the flavors we've put together for your absolutely amazing party: \n"
    "American       BBQ                East Asian\n"
    "Everyday       Global Cuisine     Healthy\n"
    "Home-Cooking   Innovative         Italian\n"
    "Latin          Misc.              Modern American\n"
    "Rustic         Southern Comfort   South Asian\n"
    "Sweet Treats   Trad. Home-Cooking")
    response = input("Please enter a single flavor so we can pull up a list "
    "of chefs from FoodNetwork for you! ")
    while response not in flavors:
        response = input("Whoops! That doesn't look quite right, please try again! ")
    if response == "exit":
        print("Bye! Hope your party's a blast!")
        exit()
    flavor_chef = process_flavors(response)
    num_chef = 0
    print("-"*40, "\n", "CHEFS WITH A ", response, " FLAVOR", "\n", "-"*40)
    for f in flavor_chef:
        num_chef +=1
        print(str(num_chef) + ". " + f)
    print("Cool! So you've got a couple of options now! Path 1: You can choose a chef to look at or we can give you"
    "a dish from this flavor! Path 2: You can open a plotly pie chart showing the amount of recipes"
    "each of these chefs have! Which one do you want to do?")
    response = str(input("Enter '1' or '2' for either path: "))
    while response not in one_two:
        response = input("Enter '1' or '2' for either path: ")
    if response == '1':
        chef_dish(flavor_chef)
    elif response == '2':
        pie_chart(flavor_chef)
        print("Alright now let's choose a chef/dish!")
        chef_dish(flavor_chef)
    elif response == 'exit':
        print("Bye! Hope your party's a blast!")
        exit()
    return flavor_chef

def chef_dish(flavor_chef):
    chef_dish = ["chef", "dish", "exit"]
    kinds = ["Snack", "Side Dish", "Main Dish", "Dessert", "exit"]
    response = input("Enter 'chef' or 'dish': ")
    while response not in chef_dish:
        response = input("Please enter 'chef' or 'dish': ")
    if response == "exit":
        print("Bye! Hope your party's a blast!")
        exit()
    elif response == 'chef':
        response = input("Nice! Type in the name of the chef you want to look at: ")
        while response not in flavor_chef:
            response = input("Oops! Did you type that in right? Try again: ")
        if response == "exit":
            print("Bye! Hope your party's a blast!")
            exit()
        chef(response)
    elif response == 'dish':
        print("Solid! Do you want a snack, side, main dish, or dessert?")
        response = input("Please enter 'Snack', 'Side Dish', 'Main Dish', or 'Dessert': ")
        while response not in kinds:
            response = input("Oops! Did you type that in right? Try again: ")
        if response == "exit":
            print("Bye! Hope your party's a blast!")
            exit()
        dish(response)
    return 0

def dish(kind):
    music_flavor = ["music", "flavor"]
    yes_no = ["yes", "no", "exit"]
    one_two = ["1", "2", "exit"]
    print("-"*15, "\n", "A ", kind, "DISH" "\n", "-"*15)
    dish = process_dish(kind)
    for d in dish:
        for i in d:
            formatted = i + " --- " + d[i][2] + ", " + d[i][1] + ", Level: " + d[i][3].replace(" ", "")
            print(formatted)
    print("\n Do you want to go to the url for this dish?")
    response = input("Enter 'yes' to go to the url or enter 'no' to go back to flavors: ")
    while response not in yes_no:
        response = input("Please enter 'yes' or 'no': ")
    if response == "yes":
        for d in dish:
            url = d[i][0]
            print("Launching " + url + " in browser!")
            webbrowser.open(url)
            print("Are you satisfied with your recipe? Do you want to go look at music?")
            response = input("Enter 'music' for music or enter 'flavor' to go back to the flavors ")
            while response not in music_flavor:
                response = input("Please try again: ")
            if response == 'music':
                response = input("Enter a search term for Spotify: ")
                spotify = get_spotify_playlist(response)
                bar_graph_spotify(spotify)
            elif response == 'flavor':
                flavor_chef = flavors()
                print("Cool! So you've got a couple of options now! Path 1: You can choose a chef to look at or we can give you "
                " a dish from this flavor! Path 2: You can open a plotly pie chart showing the amount of recipes "
                " each of these chefs have! Which one do you want to do?")
                response = str(input("Enter '1' or '2' for either path: "))
                while response not in one_two:
                    response = input("Enter '1' or '2' for either path: ")
                if response == '1':
                    chef_dish(flavor_chef)
                if response == '2':
                    pie_chart(flavor_chef)
    elif response == "no":
        flavor_chef = flavors()
        chef_dish(flavor_chef)
    elif response == "exit":
        print("Bye! Hope your party's a blast!")
        exit()
    return 0


def chef(name):
    music_flavor = ["music", "flavor", "exit"]
    one_two = ["one", "two", "exit"]
    num_chef_dish = 0
    print("-"*30, "\n", "DISHES BY ", name, "\n" + "-"*30)
    dishes_o_chefs = process_chef(name)
    dish_nums = []
    for d in dishes_o_chefs:
        for i in d:
            num_chef_dish += 1
            formatted = str(num_chef_dish) + ". " + i + " --- " + d[i][2] + ", " + ", Type: " + d[i][1] + ", Level: " + d[i][3].replace(" ", "")
            print(formatted)
            dish_nums.append((num_chef_dish - 1, d[i][0]))
    response = input("Enter a number to go to that dish's url, enter 'flavor' to go back to the flavors, or"
    "enter 'graph' to see a graph of this chef's number of main, side, snack, and dessert dishes! ")
    if response == "flavor":
        flavor_chef = flavors()
        chef_dish(flavor_chef)
    elif response.isdigit() == True:
        # try:
        url = dish_nums[(int(response)-1)][1]
        print(url)
        print("Launching " + url + " in browser!")
        webbrowser.open(url)
        # except:
        #     print("URL Unknown")
        print("Are you satisfied with your recipe? Do you want to go look at music?")
        response = input("Enter 'music' for music or enter 'flavor' to go back to the flavors ")
        while response not in music_flavor:
            response = input("Please try again: ")
        if response == 'music':
            response = input("Enter a search term for Spotify: ")
            get_spotify_playlist(response)
        elif response == 'flavor':
            flavor_chef = flavors()
            print("Cool! So you've got a couple of options now! Path 1: You can choose a chef to look at or we can give you"
            " a dish from this flavor! Path 2: You can open a plotly pie chart showing the amount of recipes"
            " each of these chefs have! Which one do you want to do?")
            response = str(input("Enter '1' or '2' for either path: "))
            while response not in one_two:
                response = input("Enter '1' or '2' for either path: ")
            if response == '1':
                chef_dish(flavor_chef)
            elif response == '2':
                pie_chart(flavor_chef)
                print("Great! Let's go look at some chef/dishes from this flavor now!")
                chef_dish(flavor_chef)
            elif response == "exit":
                print("Bye! Hope your party's a blast!")
                exit()
        elif response == "exit":
            print("Bye! Hope your party's a blast!")
            exit()
    elif response == 'graph':
        bar_graph_type(name)
        print("Nice!")
        response = input("Enter a number to go to that dish's url, enter 'flavor' to go back to the flavors, or"
        "enter 'graph' to see a graph of this chef's number of main, side, snack, and dessert dishes! ")
        if response == "flavor":
            flavor_chef = flavors()
            chef_dish(flavor_chef)
        elif response.isdigit() == True:
            #try:
            url = dish_nums[(int(response)-1)][1]
            print(url)
            print("Launching " + url + " in browser!")
            webbrowser.open(url)
            # except:
            #     print("URL Unknown")
            print("Are you satisfied with your recipe? Do you want to go look at music?")
            response = input("Enter 'music' for music or enter 'flavor' to go back to the flavors ")
            while response not in music_flavor:
                response = input("Please try again: ")
            if response == 'music':
                response = input("Enter a search term for Spotify: ")
                get_spotify_playlist(response)
            elif response == 'flavor':
                flavor_chef = flavors()
                print("Cool! So you've got a couple of options now! Path 1: You can choose a chef to look at or we can give you"
                "a dish from this flavor! Path 2: You can open a plotly pie chart showing the amount of recipes"
                "each of these chefs have! Which one do you want to do?")
                response = str(input("Enter '1' or '2' for either path: "))
                while response not in one_two:
                    response = input("Enter '1' or '2' for either path: ")
                if response == '1':
                    chef_dish(flavor_chef)
                if response == '2':
                    pie_chart(flavor_chef)
                    print("Great! Let's go look at some chef/dishes from this flavor now!")
                    chef_dish(flavor_chef)
        elif response == "exit":
            print("Bye! Hope your party's a blast!")
            exit()
        else:
            print("Hmmm. That doesn't seem right!")
            response = input("Enter 'flavor' to go back to the flavors! ")
            while response != 'flavor':
                print("Hmmm. That doesn't seem right!")
                response = input("Enter 'flavor' to go back to the flavors! ")
            flavor_chef = flavors()
            chef_dish(flavor_chef)
    elif response == "exit":
        print("Bye! Hope your party's a blast!")
        exit()
    else:
        print("Hmmm. That doesn't seem right!")
        response = input("Enter 'flavor' to go back to the flavors! ")
        while response != 'flavor':
            print("Hmmm. That doesn't seem right!")
            response = input("Enter 'flavor' to go back to the flavors! ")
        flavor_chef = flavors()
        chef_dish(flavor_chef)

def interactive_prompt():
    one_two = ["1", "2", "exit"]
    print("-"*30, "\n", "PARTY PLANNING PROGRAM \n", "-"*30)
    print("Hey! So you wanna plan a party? Don't know where to start? Look no "
    "further! We'll help you with the two most important parts of any party: "
    "food and music! (You've gotta take care of the conversation on your own, "
    "though, sorry!)")
    response = input("Enter anything if this is the program you've been looking for "
    "your whole life (enter 'exit' if you want to leave!): ")
    if response == "exit":
        print("Bye! Hope your party's a blast!")
        exit()
    print("With P^3 you can get delicious recipes and great music for the "
    "best party you've ever thrown. Yes, even better than your neighbor Janet's "
    "Halloween party last year.")
    response = input("Cool right? ")
    if response == 'exit':
        print("Bye! Hope your party's a blast!")
        exit()
    print("Yea, we think so too. Let's get started.")
    flavor_chef = flavors()


if __name__=="__main__":
    #get_dish_info()
    #init_db()
    #insert_data()
    interactive_prompt()
    #get_spotify_playlist("country")
