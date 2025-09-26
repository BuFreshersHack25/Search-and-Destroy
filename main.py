import os,bcrypt,re,base64,time,subprocess
from supabase import create_client, Client
from dotenv import load_dotenv
from postgrest.exceptions import APIError
from flask import Flask,make_response,request,render_template,redirect,url_for,session,jsonify
from pyngrok import ngrok

app = Flask(__name__)



load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
ngrok.set_auth_token(os.environ.get("NGROK_API_KEY"))


supabase: Client = create_client(url,key)
#print(bcrypt.hashpw("hashed_pw_1".encode("utf-8"), bcrypt.gensalt(14)))

def login(username: str, password: str):
    try:
        response = supabase.table("users").select("password").eq("username", username).execute()
        #print(response)
        if response.data:
            stored_hash = response.data[0]["password"].encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
    except IndexError:
        return "username"
    except Exception:
        return "support"

def register(username,password,email):
    try:
        if re.fullmatch(R"[^@]+@[^@]+\.[^@]+",email) == None:
            print("invalid email address")
            return "e"
        if re.fullmatch(R"^(?=.*[A-Za-z])(?=.*\d).{8,}$",password) == None:
            print("password must at least contain:8 chars,one number and one letter")
            return "p"
        else:
            supabase.table("users").insert({
                "username": username,
                "password" :bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14)).decode("utf-8"),
                "email": email}).execute()
            return True
  
    except APIError as error: 
        if error.code == "23505":
            print("Username allready in use try another")
            return "u"
        else:
            print(error.code,type(error.code))
            return False

def start_ngrok():
    public_url = ngrok.connect(5000)  # start tunnel
    print(" * ngrok tunnel URL:", public_url)
    return public_url
start_ngrok()

@app.route('/')
def index():
  if 'username' in session:
      return render_template('index.html')
  else:
      return "<script>alert('Unauthorised access please login');window.location.replace('/login')</script>"
@app.route('/login')
def login_page():
    if 'username' in session:
         return redirect(url_for('index'))
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def log_in():
    username = request.form['username']
    password = request.form['password']
    login_state = login(username,password)
    if(login_state== True):
        session["username"] = username # lazy writing fix later,also add session id.
        return redirect(url_for('index'))
    elif(login_state == False):
        return ("<script>alert('Your username or password is incorrect'))</script>")
    elif (login_state == "username"):
        return ("<script>alert('Please check your username is correct'))</script>")
    else:
        return ("<script>alert('Please contact support'))</script>")
@app.route('/register') ## needs testing on flask
def reg_page():
    if 'username' in session:
      return render_template('index.html')
    return render_template('register.html',invld_u = "none",invld_e = "none",invld_p = "none")
@app.route('/register', methods=['POST'])
def sign_up():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    state = register(username,password,email)
    if(state == True):
        session['username'] = username
        return "<script>alert('Successfully registered');window.location.replace('/index')</script>"
    elif(state == "u"):
        return render_template("register.html",invld_u = "hidden", invld_p = "none",invld_e = "none")
    elif(state == "p"):
        return render_template("register.html",invld_u = "none", invld_p = "block",invld_e = "none")
    elif(state == "e"):
        return render_template("register.html",invld_u = "none", invld_p = "none",invld_e = "block")
    else:
        return "<script>alert('If you do not allready have an account with this email please contact support.');window.location.replace('/login');</script>"
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for("log_in"))

@app.route('/leaderboard')
def leaderboard():
     if 'username' not in session:
         return redirect(url_for('log_in'))
     return render_template("leaderboard.html")

@app.route('/leaderboard_data')
def get_leaderboard_data():
        response = supabase.from_('leaderboard').select(
        'score, users(username)'
        ).order(
            'score', desc=True
        ).execute()
        leaderboard_data = response.data
        current_username = session["username"]
        formatted_data = [
            {
                'username': "You" if current_username and player['users']['username'] == current_username else player['users']['username'],
                'score': player['score']
            } 
            for player in leaderboard_data
        ]
        return jsonify(formatted_data)

@app.route('/image', methods=['POST'])
def image():
  current_time = time.time()
  filename = str(current_time) + ".jpeg"
  imagedata = request.data[23:]
  with open(filename, "wb") as img:
    img.write(base64.decodebytes(imagedata))