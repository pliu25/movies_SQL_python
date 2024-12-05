import sqlite3
import random
import json

from User_Model_starter import User
from Game_Model_starter import Game

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
            
            #print("user_id", user_id)
            categories = json.dumps(Scorecard.create_blank_score_info(self))
            results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE game_id = {game_id};").fetchall()
            game_count = len(results)
            turn_order = game_count + 1

            if turn_order > 4:
                return {"status": "error",
                    "data": "too many scorecards initiated! 4 max players"
                    }
            
            player_exists = cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id} AND game_id = {game_id};").fetchall()

            if player_exists:
                return {"status": "error",
                    "data": "scorecard already initiated for existing player!"
                    }
            
            sc_data = (card_id, game_id, user_id, categories, turn_order, name)
            print(sc_data)
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?);", sc_data)
            db_connection.commit()

            return {"status": "success",
                    "data": self.to_dict(sc_data)
                    }
            

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get(self, name = None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if name:
                sc_info = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?;", (name,)).fetchone()

                if sc_info:
                    return {"status": "success",
                        "data": self.to_dict(sc_info)}
                else:
                    return {"status": "error",
                        "data": "scorecard not found!"}


            if id: 
                sc_info = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,)).fetchone()

                if sc_info:
                    return {"status": "success",
                        "data": self.to_dict(sc_info)}
                else:
                    return {"status": "error",
                        "data": "scorecard not found!"}
            
            else:
                return {"status": "error",
                        "data": "scorecard name or id not provided!"}
            
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            fetch_all_cards = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            all_cards = []
            for card_data in fetch_all_cards:
                all_cards.append(self.to_dict(card_data))
            #print("all_users", all_cards)
            return {"status":"success",
                    "data":all_cards}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all_game_scorecards(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            all_cards = self.get_all()["data"]
            game_cards = []
            for card in all_cards:
                card_game_name = card["name"].split("|")[0]
                if card_game_name == game_name:
                    game_cards.append(card_game_name)

            print("game_cards", game_cards)
            return {"status":"success",
                    "data":game_cards}



        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_game_usernames(self, game_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            all_cards = self.get_all()["data"]
            usernames = []
            for card in all_cards:
                card_game_name = card["name"].split("|")[0]
                card_username = card["name"].split("|")[1]
                if card_game_name == game_name:
                    usernames.append(card_username)

            return {"status":"success",
                    "data":usernames}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_user_game_names(self, username:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            all_cards = self.get_all()["data"]
            game_cards = []
            for card in all_cards:
                card_game_name = card["name"].split("|")[0]
                card_username = card["name"].split("|")[1]
                if card_username == username:
                    game_cards.append(card_game_name)

            return {"status":"success",
                    "data":game_cards}
            
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

    print(Scorecards.create_blank_score_info)