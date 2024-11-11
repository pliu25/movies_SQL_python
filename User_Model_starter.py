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
            sql_cmd = f'SELECT id, username FROM {self.table_name} WHERE EXISTS'
            #sql_cmd_test = 'SELECT db_name'.format(self)
            print(self.table_name)
            print("sql_cmd", sql_cmd)
            with db_connection:
                results = cursor.execute(sql_cmd)
                data = results.fetchone()
                print("data", data)
            if data == 0:
                return {"status":"success",
                    "data":False}
            else:
                return {"status":"success",
                    "data":True}
            '''
            if id < self.max_safe_id:
                return {"status":"success",
                    "data":True}
            elif type(username) == str:
                return {"status":"success",
                    "data":True}
            elif (username == "") or (id == ""):
                return {"status":"success",
                    "data":False}

            print(self.db_name)
            '''
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

            # TODO: check to see if id already exists!! return error 


            
            user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()
            #return list of dictionaries 
            new_query = f"SELECT * FROM {self.table_name}"
            print("new_query", new_query)
            DB_output = cursor.execute(new_query)
            #username_output = cursor.execute(usernames)
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
            new_query = f"SELECT * FROM {self.table_name}"
            DB_output = cursor.execute(new_query)
            print(self.db_name)
            return {"status":"success",
                    "data":len(self.db_name)}
        
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