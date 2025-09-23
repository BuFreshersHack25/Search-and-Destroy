import os,bcrypt,re
from supabase import create_client, Client
from dotenv import load_dotenv
from postgrest.exceptions import APIError

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")


supabase: Client = create_client(url,key)
#print(bcrypt.hashpw("hashed_pw_1".encode("utf-8"), bcrypt.gensalt(14)))

def login(username: str, password: str) -> bool:

    response = supabase.table("users").select("password").eq("username", username).execute()
    print(response)

    if response.data:
        stored_hash = response.data[0]["password"].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
    elif (response.data[0] != None):
         return response.data[0]["password"] == password

def register(username,password,email):
    try:
        if re.fullmatch(R"[^@]+@[^@]+\.[^@]+",email) == None:
            print("invalid email address")
            return False
        if re.fullmatch(R"^(?=.*[A-Za-z])(?=.*\d).{8,}$",password) == None:
            print("password must at least contain:8 chars,one number and one letter")
            return False
        else:
            supabase.table("users").insert({
                "username": username,
                "password" :bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14)).decode("utf-8"),
                "email": email}).execute()
            return True
  
    except APIError as error: 
        if error.code == 2305:
            print("Username allready in use try another")
            return False
        else:
            print(error)
            return False



username = "bob"
password_input = "hashed_pw_2"

print(register("steve","hashed_pw_4","steve@googlemail.com"))