import unittest
from final_food import *

class TestDatabase(unittest.TestCase):

    def test_chef_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT LastName FROM Chefs'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Burrell',), result_list)
        self.assertEqual(len(result_list), 136)

        sql = '''
            SELECT FirstName, LastName, ChefUrl,
                   PopularRecipe, FlavorProfile
            FROM Chefs
            WHERE FirstName="Marc"
            ORDER BY LastName DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 3)
        self.assertEqual(result_list[0][1], "Summers")

        conn.close()

    def test_dish_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT DishName
            FROM Dishes
            WHERE Type="Main Dish"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Pulled Pork with Mango BBQ Sauce',), result_list)
        #self.assertEqual(len(result_list), 27)

        sql = '''
            SELECT COUNT(*)
            FROM Dishes
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        #self.assertEqual(count, 250)

        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT c.FirstName
            FROM Chefs as c
                JOIN Dishes as d
                ON c.ID=d.ChefID
            WHERE d.DishName="Maple Pig Cocktail"
                AND c.LastName="Fieri"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Guy',), result_list)
        conn.close()
class TestProcessFlavor(unittest.TestCase):
    def test_process_flavor(self):
        results = process_flavor('American')
        self.assertIn('Aaron McCargo Jr.',results)

        results = process_flavor('Sweet Treats')
        self.assertEqual(len(results), 8)
        self.assertIn('Warren Brown', results)

class TestProcessChef(unittest.TestCase):
    def test_process_chef(self):
        results = process_chef('Jeff Corwin')
        self.assertEqual(len(results[0]),4)

        results = process_chef('Keegan Gerhard')
        self.assertEqual(results[1][2], '5 out of 5')
        self.assertEqual(results[0][0], "Jeff's Fresh Black Bean Salsa")

class TestProcessDish(unittest.TestCase):
    def test_process_dish(self):
        results = process_dish('Cupcake Tree')
        self.assertEqual(results[0][2],'2 out of 5')

        results = process_dish('Tropical Trifle')
        self.assertEqual(results[0][3], 'Dessert')
        self.assertEqual(results[0][4], 'Intermediate')

class TestSpotify(unittest.TestCase):
    def test_spotify(self):
        search_term = "love"
        results = get_spotify_playlist(search_term)
        self.assertEqual(len(results),5)

        search_term = "latin"
        results = get_spotify_playlist(search_term)
        self.assertIn("Latin Cardio", results)
