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
            '''
                Insert your code here
            '''
            '''
            if not username and not id:
                return {"status":"error",
                    "data": "failed to provide username or id"}
            '''
            
            if username:
                #exists_check = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = ?", (username,)).fetchall()
                exists_check = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = {username}").fetchall()
                #exists_check = cursor.execute('SELECT * FROM "{}" WHERE username = ?'.format(self.table_name.replace('"', '""')), (username,)).fetchall()
                #print("username", username)
                print("exists_check_username", exists_check)
                print("exists_check_username2", f"SELECT * FROM {self.table_name} WHERE username = {username}")
             
            if id:
                exists_check = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id,)).fetchall()
                #exists_check = cursor.execute('SELECT * FROM "{}" WHERE id = ?'.format(self.table_name.replace('"', '""')), (id,)).fetchall()

            #print("exists_check", exists_check)
            if exists_check:
               return {"status":"success",
                    "data": True}
            else:
                return {"status":"success",
                    "data": False}    
                
            #return {"status":"error",
                    #"data": "failed to provide username or id"}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
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

            user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            '''
            user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()
            #return list of dictionaries 
            new_query = f"SELECT * FROM {self.table_name}"
            #print("new_query", new_query)
            DB_output = cursor.execute(new_query)
            #username = f"SELECT username * FROM {self.table_name}"
            #username_output = cursor.execute(username)
            #print("username", username_output)
            #print("fetchall2", username_output.fetchall())
            print("fetchall",DB_output.fetchall())
            if user_data[0] < self.max_safe_id:
                #if user_data[2].isalnum() or user_data[2].includes("_") or user_data[2].includes("-"):
                    #if user_data[2] != self.users[2]["email"]
                    return {"status": "success",
                    "data": self.to_dict(user_data)
                    }
            else: 
                return {"status": "error",
                    "data": self.to_dict(user_data)
                    }
            '''
        
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
            sql_select = f"SELECT * FROM {self.table_name};"
            users_data = cursor.execute(sql_select).fetchall()
            all_users = []
            for user_data in users_data:
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
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db" #f"{os.getcwd()}/Models/yahtzeeDB.db"
    table_name = "users"
    print("DB_location", DB_location)
    Users = User(DB_location, table_name) 
    Users.initialize_table()

    user_details={
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"123TriniT"
    }
    exists = Users.exists(user_details)
    print("exists", exists)
    results = Users.create(user_details)
    print("returned user",results)
    get_all = Users.get_all()
    print("get_all", get_all)