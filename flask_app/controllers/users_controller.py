from flask_app import app
from flask import  render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  
from flask_app.models.user import User
from flask_app.models.recipe import Recipe




#=======================================================

#               Home Route/Home Page

#=======================================================

@app.route("/")
def index():
    # call the get all classmethod to get all users
    
    return render_template("login_reg.html")


#=========================================================

#                     Register Route

#=========================================================

@app.route("/register", methods=["POST"])
def register():
    # print("start registration")
    #1 - validate information
    if not User.validate_register(request.form):

        return redirect("/") #this one is indented to be within the if statement
    # print("validation good")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    # print(client_id)

    return redirect('/user/dashboard') #this is like the "else" portion of statement, taking people to their acct./dashboard if they successfully login.


#======================================================

#                     Login Route

#======================================================


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    if not User.validate_login(request.form):
        return redirect("/")

    #2 pull user data and log them in
    logged_user=User.get_by_email(request.form)

    session['user_id'] = logged_user.id 
    
    # never render on a post!!!
    return redirect("/user/dashboard")




#===================================================

#                 User Dashboard Route

#===================================================

@app.route("/user/dashboard")
def user_dashboard():

    if 'user_id' not in session: 
        flash("Please login or register before proceeding!")
        return redirect ('/')

    query_data ={
        "id" : session["user_id"]  #"id" is a key name that must match what is on the model side
    }

    user=User.get_by_id(query_data)
    recipes= Recipe.get_all_recipes()

    return render_template("user_dashboard.html", user=user, recipes=recipes)



#=======================================================

#               Shop Page

#=======================================================

@app.route("/shop")
def shop():
    # call the get all classmethod to get all users
    
    return render_template("shop.html")




#=======================================================

#               Shop Page

#=======================================================

@app.route("/cart")
def cart():
    # call the get all classmethod to get all users
    
    return render_template("cart.html")





#=======================================================

#                 Session Clear/Logout Route

#=======================================================

@app.route("/logout")
def logout():  
    session.clear()
    return redirect("/")