import os
from supabase import create_client, Client
import bcrypt
from dotenv import load_dotenv
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")


supabase: Client = create_client(url,key)
#print(bcrypt.hashpw("hashed_pw_1".encode("utf-8"), bcrypt.gensalt(14)))

def check_password(username: str, password: str) -> bool:

    response = supabase.table("users").select("password").eq("username", username).execute()
    print(response)

    if response.data:
        stored_hash = response.data[0]["password"].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
    elif (response.data[0] != None):
         return response.data[0]["password"] == password

username = "bob"
password_input = "hashed_pw_2"

print(check_password(username,password_input))