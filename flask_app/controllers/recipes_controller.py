from flask_app import app
from flask import  render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


#================================================

#                  Add Recipe Route

#================================================

@app.route("/add/new/recipe")
def add_new_recipe():
    if 'user_id' not in session:
        flash("Please login or register before proceeding!")
        return redirect ('/')
    user_data={
        "id": session["user_id"]
    }
    user=User.get_by_id(user_data)
    return render_template("recipes_dashboard.html", user=user)


#================================================

#           Add New Recipe POST Route

#================================================

@app.route("/add/recipe", methods=["POST"])
def add_recipe():
    if not Recipe.validate_new_recipe_maker(request.form): #will need this in edit route as well

        return redirect("/")
    data= {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_added": request.form["date_added"],
        "users_id": session["user_id"]  #this allows whoever creates a recipe to be attached to it.
    } #"users_id" on the left of colon is a name that must match the data in blue in the model. In the session brackets i.e session["user_id"] must match what I called when the user logged in. So in other words, on the user controller side I named the user_id without the "s" therefore must call it that everytime place "user_id" w/in session.
    Recipe.save(data)
    return redirect('/user/dashboard')


#================================================

#            Show Recipe Route

#================================================

@app.route("/show/recipe/<int:id>")
def show_recipe(id):
    
    data={
        "id": id
    }
    user_data={
        "id": session["user_id"]
    }
    recipe=Recipe.get_by_id(data)
    user=User.get_by_id(user_data)

    return render_template("user_dashboard.html", recipe=recipe, user=user)


#=====================================================

#                  Edit Recipe POST Route

#======================================================
#Don't forget to place the url into the html action method properly too i.e action="/edit/recipe/{{id}}"
@app.route("/edit/recipe/<int:id>", methods=["POST"])
    #Note:if pass id in the url must pass it into the function as well!
def edit_recipe(id):
    print("=======================================")
    if not Recipe.validate_new_recipe_maker(request.form): #will need this in edit route as well

        return redirect("/")

    data= { 
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_added": request.form["date_added"]
    }
    Recipe.edit_recipe(data)
    return redirect("/user/dashboard")


#=====================================================

#                  Edit Recipe Render Route

#======================================================

@app.route("/update/recipe/<int:id>")
def update_recipe(id):
    if 'user_id' not in session:
        flash("Please login or register before proceeding!")
        return redirect ('/')

    data={
        "id": id
    }
    recipe=Recipe.get_by_id(data)
    return render_template("edit_recipe.html", recipe=recipe)





#=====================================================

#                  Delete Recipe Route

#======================================================

@app.route("/delete/recipe/<int:id>")
def delete_recipe(id):

    data={
        "id": id
    }
    Recipe.delete_recipe(data)  #don't need aything else because we dont return anything on a delete and an insert as well as my creates.
    return redirect("/user/dashboard") #may not need the recipe=recipe part but put it anyway.