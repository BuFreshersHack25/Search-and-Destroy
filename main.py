import os,bcrypt,re,base64,time
from supabase import create_client, Client
from dotenv import load_dotenv
from postgrest.exceptions import APIError
from flask import Flask,Response,request,render_template,redirect,url_for,session
app = Flask(__name__)

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")



supabase: Client = create_client(url,key)
#print(bcrypt.hashpw("hashed_pw_1".encode("utf-8"), bcrypt.gensalt(14)))

def login(username: str, password: str):
    try:
        response = supabase.table("users").select("password").eq("username", username).execute()
        #print(response)
        if response.data:
            stored_hash = response.data[0]["password"].encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
        elif (response.data[0] != None):
            return response.data[0]["password"] == password
    except IndexError:
        print("Please check your username is valid")
    except Exception:
        print("Please contact support" + Exception)

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


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def log_in():
    username = request.form['username']
    password = request.form['password']
    print(password,type(password))
    if(login(username,password)== True):
        session["username"] = username # lazy writing fix later,also add session id.
        return redirect(url_for('index'))
    else:
        print(type(username)) ## needs to redirect errors correctly
        return username
@app.route('/register') ## needs testing on flask
def reg_page():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def sign_up():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    return register(username,password,email) #deal with this
username = "bob"
password_input = "hashed_pw_2"
@app.route('/image', methods=['POST'])
def image():
  current_time = time.time()
  filename = str(current_time) + ".jpeg"
  imagedata = request.data[23:]
  with open(filename, "wb") as img:
    img.write(base64.decodebytes(imagedata))

print(login("steve","hashed_pw_4"))