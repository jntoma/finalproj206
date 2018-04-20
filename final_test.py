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
        self.assertEqual(len(result_list), 137)

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
        self.assertIn(('Sweet Hot Fried Chicken and Waffles',), result_list)
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
            WHERE d.DishName="Dirty P's Garlic-Ginger Chicken Thighs"
                AND c.LastName="Fieri"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Guy',), result_list)
        conn.close()
class TestProcessFlavor(unittest.TestCase):
    def test_process_flavor(self):
        results = process_flavors('American')
        self.assertIn('Aaron McCargo Jr.',results)

        results = process_flavors('Sweet Treats')
        self.assertEqual(len(results), 8)
        self.assertIn('Warren Brown', results)

class TestProcessChef(unittest.TestCase):
    def test_process_chef(self):
        results = process_chef('Jeff Corwin')
        self.assertEqual(len(results[0]),1)

        results = process_chef('Keegan Gerhard')
        self.assertEqual(results[1]["Meringue"][1], '5 out of 5')
        self.assertEqual(results[0]["Meringue"][2], "Dessert")

class TestProcessDish(unittest.TestCase):
    def test_process_dish(self):
        results = process_dish('Main Dish')
        self.assertEqual(results[0]["Sweet Hot Fried Chicken and Waffles"][1],'5 out of 5')

        results = process_dish('Dessert')
        self.assertEqual(results[0]["Coconut Toffee"][2], 'Dessert')

class TestScraping(unittest.TestCase):
    def test_get_chef(self):
        results = get_chef_info()
        self.assertEqual(len(results),135)

unittest.main()
