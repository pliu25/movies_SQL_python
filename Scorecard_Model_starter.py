import sqlite3
import random
import json

from User_Model import User
from Game_Model import Game

class Scorecard:
    def __init__(self, db_name, scorecard_table_name, user_table_name, game_table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = scorecard_table_name 
        self.user_table_name = user_table_name
        self.game_table_name = game_table_name
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name, )
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    game_id INTEGER,
                    user_id INTEGER,
                    categories TEXT,
                    turn_order INTEGER,
                    name TEXT,
                    FOREIGN KEY(game_id) REFERENCES {self.game_table_name}(id) ON DELETE CASCADE,
                    FOREIGN KEY(user_id) REFERENCES {self.user_table_name}(id) ON DELETE CASCADE
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create(self, game_id, user_id, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            card_id = random.randint(0, self.max_safe_id)
   
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get(self, name = None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all_game_scorecards(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_game_usernames(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_user_game_names(self, username:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, id, name=None, categories=None): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, id): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, card_tuple):
        game_dict={}
        if card_tuple:
            game_dict["id"]=card_tuple[0]
            game_dict["game_id"]=card_tuple[1]
            game_dict["user_id"]=card_tuple[2]
            game_dict["categories"]=json.loads(card_tuple[3])
            game_dict["turn_order"]=card_tuple[4]
            game_dict["name"]=card_tuple[5]
        return game_dict
    
    def create_blank_score_info(self):
        return {
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }

    def tally_score(self, score_info):
        total_score = 0
   
        return total_score

if __name__ == '__main__':
    import os
    #print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db"
    #print("location", DB_location)
    Users = User(DB_location, "users")
    Users.initialize_table()
    Games = Game(DB_location, "games")
    Games.initialize_table()
    Scorecards = Scorecard(DB_location, "scorecards", "users", "games")
    Scorecards.initialize_table()