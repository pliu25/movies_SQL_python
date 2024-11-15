# Pearl Liu #
import sqlite3
import random
from datetime import datetime

class Game:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE,
                    created TIMESTAMP,
                    finished TIMESTAMP
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, game_name = None, id = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
            if email:
                    exists_check = cursor.execute(
                        f"SELECT * FROM {self.table_name} WHERE email = ?;", (email,)
                    ).fetchall() 
            elif not username and not id:
                    return {"status": "error", "data": "username or id not provided!"}
            '''   

            if not game_name:
                return {"status": "error", "data": "username or id not provided!"}

            #check if name exists
            if game_name:
                exists_check = cursor.execute(
                    f"SELECT * FROM {self.table_name} WHERE name = ?;", (game_name,)
                ).fetchall()
                #print("exists_check_username:", exists_check)
            
            #check if id exists
            if id:
                exists_check = cursor.execute(
                    f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,)
                ).fetchall()
   
            # check
            if len(exists_check) > 0:
                return {"status": "success", "data": True}
            else:
                return {"status": "success", "data": False}

        except sqlite3.Error as error:
            return {"status": "error", "data": error}
        finally:
            db_connection.close() 
    
    def create(self, game_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game_id = random.randint(0, self.max_safe_id)

            print("game_info", game_info)
            # TODO: check to see if id already exists!! return error 
            
            if self.exists(id = game_id)["data"] == True:
                return {"status":"error",
                    "data":"error: id already exists"}
            
            if self.exists(game_name = game_info["name"])["data"] == True:
                return {"status": "error",
                    "data": "error: game name already exists"}
            #print("exists_check", self.exists(email = game_info["email"])["data"])
            
            #validity checks
            for char in game_info["name"]:
                if not (char.isalnum() or char == "-" or char == "_"):
                    return {"status": "error",
                            "data": "bad game name: game names can only include A-Z, a-z, 0-9, -, _"
                            }

            created_date = datetime.now()

            game_data = (game_id, game_info["name"], created_date, created_date)
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", game_data)
            db_connection.commit()

            return {"status": "success",
                    "data": self.to_dict(game_data)
                    }
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, game_name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                #Insert your code here
            '''

            if game_name:
                if self.exists(game_name=game_name)["data"] == False:
                    return {"status": "error",
                        "data": "game with this name does not exist!"}
                
                fetch_game_name = cursor.execute(
                    f"SELECT * FROM {self.table_name} WHERE name = ?;", (game_name,)
                ).fetchone()
                return {"status": "success",
                        "data": self.to_dict(fetch_game_name)}


            if id: 
                if self.exists(id=id)["data"] == False:
                    return {"status": "error",
                        "data": "game with this id does not exist!"}
                
                fetch_id = cursor.execute(
                    f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,)
                ).fetchone()
                return {"status": "success",
                        "data": self.to_dict(fetch_id)}
            
            else:
                return {"status": "error",
                        "data": "username or id not provided!"}


        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                #Insert your code here
            '''
            fetch_all_games = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            all_games = []
            for game_data in fetch_all_games:
                all_games.append(self.to_dict(game_data))
            print("all_users", all_games)
            return {"status":"success",
                    "data":all_games}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def is_finished(self, game_name) :
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game_id = random.randint(0, self.max_safe_id)

            # TODO: check to see if id already exists!! return error 
            #check if created time and finished time is different (update updates this time)
            

            #return {"status": "success",
                #"data": self.to_dict(game_data)
                    #}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()

    def update(self, game_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                #Insert your code here
            '''
            print("game_info", game_info)
            if not game_info:
                return {"status":"error",
                    "data": "game info not provided!"}
            
            if self.exists(id = game_info["id"])["data"] == True:
                for column in game_info:
                    if column != "id":
                        
                        cursor.execute(f"UPDATE {self.table_name} SET {column} = ? WHERE id = ?;", (game_info[column], game_info["id"]))
                        cursor.execute(f"UPDATE {self.table_name} SET {column} = ? WHERE finished = ?;", (game_info[column], datetime.now()))
                        db_connection.commit()

                return {"status":"success",
                    "data": self.get(id = game_info["id"], finished = game_info["finished"])["data"]}
            
            else:
                return {"status":"error",
                    "data": "updated information doesn't exist!"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, username): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                #Insert your code here
            '''

            if (self.exists(username=username)["data"] == True):
                remove_user = self.get(username=username)["data"]
                cursor.execute(f"DELETE FROM {self.table_name} WHERE username = '{username}';")
                db_connection.commit()

                return {"status":"success",
                        "data":remove_user}
            else:
                return {"status":"error",
                    "data":"username doesn't exist!"}
            
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, user_tuple):
        '''#Utility function which converts the tuple returned from a SQLlite3 database
           #into a Python dictionary
        '''
        user_dict={}
        if user_tuple:
            user_dict["id"]=user_tuple[0]
            user_dict["name"]=user_tuple[1]
            user_dict["created"]=str(user_tuple[2])
            user_dict["finished"]=str(user_tuple[3])
        return user_dict
    
if __name__ == '__main__':
    '''
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db" #f"{os.getcwd()}/Models/yahtzeeDB.db"
    table_name = "users"
    #print("DB_location", DB_location)
    Users = User(DB_location, table_name) 
    Users.initialize_table()

    user_details={
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"123TriniT"
    }
    exists = Users.exists(username = user_details["username"])
    print("exists", exists)
    results = Users.create(user_details)
    print("returned user",results)
    get_all = Users.get_all()
    print("get_all", get_all)
    '''
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db"
    table_name = "games"
    
    Games = Game(DB_location, table_name) 
    Games.initialize_table()

    game_details={
        "name":"woohoo",
        "created":"2024-11-15 16:50:55",
        "finished":"2024-11-15 16:53:55"
    }
    create_check = Games.create(game_details)
    print("create_check", create_check)
    exists = Games.exists(game_name = game_details["name"])
    print("exists", exists)
    
    updated_game_details={
        "name":"yay",
        "created":"2024-11-15 16:50:55",
        "finished":"2024-11-15 16:53:55"
    }
    update_check = Games.create(updated_game_details)
    print("update_check", update_check)
    #print("remove", Games.remove("justingohde"))
    

