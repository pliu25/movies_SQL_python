import sqlite3
import random

class User:
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
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, username=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
        
        # Ensure at least one of username or id is provided
            if not username and not id:
                return {"status": "error", "data": "username or id not provided!"}

            # Initialize exists_check to None
            exists_check = None

            # Check by username if provided
            if username:
                exists_check = cursor.execute(
                    f"SELECT * FROM {self.table_name} WHERE username = ?;", (username,)
                ).fetchall()
                #print("exists_check_username:", exists_check)

            # Check by id if provided
            if id:
                exists_check = cursor.execute(
                    f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,)
                ).fetchall()
                #print("exists_check_id:", exists_check)

            # Determine if a match was found
            if exists_check:
                return {"status": "success", "data": True}
            else:
                return {"status": "success", "data": False}

        except sqlite3.Error as error:
            return {"status": "error", "data": error}
        finally:
            db_connection.close() 
    
        
    def create(self, user_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            user_id = random.randint(0, self.max_safe_id)

            print("user_info", user_info)
            # TODO: check to see if id already exists!! return error 
            
            if self.exists(id = user_id)["data"] == True:
                return {"status":"error",
                    "data":"error: id already exists"}
            
            if self.exists(username = user_info["username"])["data"] == True:
                return {"status":"error",
                    "data":"error: username already exists"}
            
            #validity checks
            for char in user_info["username"]:
                if char.isalpha() == False:
                    return {"status": "error",
                            "data": "bad username: no symbols or spaces"
                            }
            if len(user_info["password"]) < 8:
                return {"status": "error",
                        "data": "password too short: password must be at least 8 characters"
                        } 
            if "@" not in user_info["email"] or "." not in user_info["email"]:
                return {"status": "error",
                        "data": "bad email: email needs @ and ."} 
            
            for char in user_info["email"]:
                if char.isalpha() == False and char != '@' and char != '.' and char.isnumeric() == False:
                    return {"status": "error",
                            "data": "bad email: invalid"} 

            user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()

            return {"status": "success",
                    "data": self.to_dict(user_data)
                    }
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, username=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                Insert your code here
            '''

            if username:
                if self.exists(username=username)["data"] == False:
                    return {"status": "error",
                        "data": "player with this username does not exist!"}
                
                fetch_username = cursor.execute(
                    f"SELECT * FROM {self.table_name} WHERE username = ?;", (username,)
                ).fetchone()
                return {"status": "success",
                        "data": self.to_dict(fetch_username)}


            if id: 
                if self.exists(id=id)["data"] == False:
                    return {"status": "error",
                        "data": "player with this id does not exist!"}
                
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
                Insert your code here
            '''
            fetch_all_users = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            all_users = []
            for user_data in fetch_all_users:
                all_users.append(self.to_dict(user_data))
            print("all_users", all_users)
            return {"status":"success",
                    "data":all_users}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, user_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            '''
                Insert your code here
            '''
            if not user_info:
                return {"status":"error",
                    "data": "user info not provided!"}
            
            if self.exists(id = user_info["id"])["data"] == True:
                for column in user_info:
                    if column != "id":
                        #cursor.execute(f"UPDATE {self.table_name} SET {column} = '{user_info[column]}' WHERE id = '{user_info['id']}';")
                        cursor.execute(f"UPDATE {self.table_name} SET {column} = ? WHERE id = ?;", (user_info[column], user_info["id"]))
                        db_connection.commit()

                return {"status":"success",
                    "data": self.get(id = user_info["id"]["data"])}
            
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
                Insert your code here
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
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary
        '''
        user_dict={}
        if user_tuple:
            user_dict["id"]=user_tuple[0]
            user_dict["email"]=user_tuple[1]
            user_dict["username"]=user_tuple[2]
            user_dict["password"]=user_tuple[3]
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
    table_name = "users"
    
    Users = User(DB_location, table_name) 
    Users.initialize_table()

    user_details={
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"123TriniT"
    }
    create_check = Users.create(user_details)
    print("create_check", create_check)
    exists = Users.exists(username = user_details["username"])
    print("exists", exists)
    updated_user_details={
        "email":"pearl.liu25@trinityschoolnyc.org",
        "username": "pliu25",
        "password": "12345678"
    }
    update_check = Users.create(updated_user_details)
    print("update_check", update_check)
    print("remove", Users.remove("justingohde"))

