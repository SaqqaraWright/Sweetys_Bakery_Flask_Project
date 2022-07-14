from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Recipe:
    db='sweetys_bakery_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_added = data['date_added']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data["users_id"]

    
    @classmethod
    def save( cls , data ):
        query = "INSERT INTO recipes ( name , description, instructions, date_added, created_at, updated_at, users_id ) VALUES (%(name)s, %(description)s,  %(instructions)s, %(date_added)s, NOW(), NOW(), %(users_id)s);"
        return connectToMySQL(cls.db).query_db(query,data) #note everything on the left of "VALUES" has to match what is in the database. Everythin in blue is just whatever I want to call, they're names.

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;" #this field "user_id" must always match what is in the query_data field in the session located in the dashboard route, this case.
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        # if len(result) < 1:
        #     return False -->don't need these previous 2 line; however, just kept them just in case.
        return cls(result[0])

    @classmethod
    def delete_recipe(cls, data):
        query="DELETE FROM recipes WHERE id=%(id)s"

        return connectToMySQL(cls.db).query_db( query, data)


    @classmethod
    def edit_recipe(cls, data):
        query="UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_added=%(date_added)s  WHERE id=%(id)s"

        return connectToMySQL(cls.db).query_db( query, data)
    
    @classmethod
    def get_all_recipes(cls):
        query="SELECT * FROM recipes"
        results = connectToMySQL(cls.db).query_db( query)
        recipes=[]
        for row in results:
            recipes.append(cls(row))
        return recipes


    @staticmethod    
    def validate_new_recipe_maker(form_data):
        is_valid = True
        if len(form_data["name"]) < 3:  
            flash("Recipe name must be present!")
            is_valid = False
        if len(form_data["description"]) < 3:  
            flash("Recipe description must be present!")
            is_valid = False
        if len(form_data["instructions"]) < 3:  
            flash("Recipe instructions must be present!")
            is_valid = False
        if form_data["date_added"] == "":  
            flash("date added must be present!")
            is_valid = False
        return is_valid