from flask import render_template, jsonify, request, redirect, url_for, make_response, flash, Blueprint
import jwt
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from recipe_app import db
from recipe_app.config import Config
from recipe_app.models import Recipe, Ingredients, Categories, User
from recipe_app.forms import RecipeForm, DeleteRecipeForm
from recipe_app.utils import capitalize_title, is_logged_in, token_required, logout_early, create_recipe_dicts

recipe_routes = Blueprint('recipe_routes', __name__)

#region Home page
@recipe_routes.route("/")   
@recipe_routes.route("/recipes", methods=['GET'])
def recipes():
    page = request.args.get("page", 1, type=int)
    recipes = Recipe.query.paginate(page=page, per_page=5)
    logged_in = is_logged_in()
    recipe_items = list(enumerate(recipes.items))

    if recipes is None:
        return render_template("error_404.html")
    else:
        return render_template(
            "recipes.html", recipes=recipes, 
            capitalize_title=capitalize_title, 
            logged_in=logged_in,
            recipe_items=recipe_items)

#region User Management
@recipe_routes.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password', 'danger')
            return render_template("login.html")

        try:
            token = jwt.encode(
                {
                    'user': user.public_id, 
                    'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
                }, 
                Config.SECRET_KEY,
                algorithm="HS256"
            )
            response = make_response(redirect(url_for('recipe_routes.recipes')))
            response.set_cookie('jwt_token', token)

            return response
        except Exception as e:
            return jsonify({"message": "Invalid token"}), 403

    return render_template("login.html")

@recipe_routes.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists. Please login.', 'info')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(public_id=str(uuid4()), name=name, email=email, password=hashed_password)
            if password == confirm_password:
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully. Please login.')
                return redirect(url_for('recipe_routes.login'))
            else:
                flash('Passwords do not match. Please try again', 'info')

    return render_template('register.html')

@recipe_routes.route("/logout", methods=['GET', 'DELETE'])
@token_required
def logout():
    token = request.cookies.get('jwt_token')
    logout_early(token)
    flash("User has successfully logged out")
    return redirect(url_for('recipe_routes.recipes'))

#region Viewing Recipes
@recipe_routes.route("/recipe/<recipe_id>", methods=['GET'])
def get_recipe_by_id(recipe_id):
    recipe_by_id = Recipe.query.get_or_404(recipe_id)
    logged_in = is_logged_in()
    if recipe_by_id is None:
        return render_template("error_404.html")
    else:
        return render_template(
            "recipe_by_id.html", 
            recipe=recipe_by_id, 
            capitalize_title=capitalize_title,
            logged_in=logged_in
        )
    
@recipe_routes.route("/recipes/<string:category>", methods=['GET'])
def get_recipe_by_category(category):
    page = request.args.get("page", 1, type=int)
    recipes_by_category = Recipe.query.filter_by(category=category).paginate(page=page, per_page=5)
    logged_in = is_logged_in()
    if recipes_by_category is None:
        return render_template("error_404.html")
    else:
        return render_template("recipe_by_category.html", 
            recipes=recipes_by_category, 
            category=category, 
            capitalize_title=capitalize_title,
            logged_in=logged_in
        )

@recipe_routes.route("/index", methods=['GET'])
def index():
    recipes = Recipe.query.all()
    if recipes is None:
        return render_template("error_404.html")

    return render_template("index.html", recipes=recipes)

#region Add Recipe
@recipe_routes.route("/add-recipe", methods=['GET', 'POST'])
@token_required
def add_recipe():
    ing_list = []
    r_form = RecipeForm()

    if r_form.add_ing.data:
        r_form.ingredients.append_entry()

    if r_form.del_ing.data:
        r_form.ingredients.pop_entry()

    if r_form.create_recipe.data:
        if r_form.ingredients.data:
            for entry in r_form.ingredients.entries:
                ing_jsonified = entry.data
                ing_list.append(ing_jsonified)

            added_recipe = Recipe(
                name=r_form.name.data,
                description=r_form.description.data,
                category=r_form.category.data,
                instructions=r_form.instructions.data,
                servings=r_form.servings.data
            )
            db.session.add(added_recipe)
            db.session.flush() # get the recipe ID
            for ing in ing_list:
                added_ing = Ingredients(recipe_id=added_recipe.id, 
                                        ingredient_name=ing['ing_name'], 
                                        quantity=ing['quantity'])
                db.session.add(added_ing)
            db.session.commit()
            return redirect(url_for('recipe_routes.recipes'))
    return render_template("add_recipe.html", form=r_form)

#region Update Recipe
@recipe_routes.route("/update-recipe/<recipe>", methods=['POST', 'GET'])
@token_required
def update_recipe(recipe):
    form = RecipeForm()
    recipe = Recipe.query.get_or_404(recipe)

    if form.add_ing.data:
        form.ingredients.append_entry()

    if form.del_ing.data:
        form.ingredients.pop_entry()

    if form.create_recipe.data:
        recipe.name = form.name.data
        recipe.description = form.description.data
        recipe.category = form.category.data
        if form.ingredients.data:
            if len(form.ingredients.data) == len(recipe.ingredients):
                for i, ing in enumerate(form.ingredients.data):
                    recipe.ingredients[i].ingredient_name = ing['ing_name']
                    recipe.ingredients[i].quantity = ing['quantity']
            elif len(form.ingredients.data) > len(recipe.ingredients):
                existing_data = len(recipe.ingredients)
                for i, ing in enumerate(form.ingredients.data[:existing_data]):
                    recipe.ingredients[i].ingredient_name = ing['ing_name']
                    recipe.ingredients[i].quantity = ing['quantity']
                for i, ing in enumerate(form.ingredients.data[existing_data:]):
                    added_ing = Ingredients(recipe_id=recipe.id, 
                                        ingredient_name=ing['ing_name'], 
                                        quantity=ing['quantity'])
                    db.session.add(added_ing)
            elif len(form.ingredients.data) < len(recipe.ingredients):
                existing_data = len(form.ingredients.data)
                for i, ing in enumerate(form.ingredients.data):
                    recipe.ingredients[i].ingredient_name = ing['ing_name']
                    recipe.ingredients[i].quantity = ing['quantity']
                for ing in recipe.ingredients[existing_data:]:
                    db.session.delete(ing)
        recipe.instructions = form.instructions.data
        recipe.servings = form.servings.data
        db.session.commit()
        return redirect(url_for('recipe_routes.recipes'))
    elif request.method == 'GET':
        if recipe.ingredients:
            form.ingredients.entries[0].form.quantity.data = recipe.ingredients[0].quantity
            form.ingredients.entries[0].form.ing_name.data = recipe.ingredients[0].ingredient_name
            for ing in recipe.ingredients[1:]:
                form.ingredients.append_entry({'quantity': ing.quantity, 'ing_name': ing.ingredient_name})
            form.name.data = recipe.name
            form.description.data = recipe.description
            form.category.data = recipe.category
            form.instructions.data = recipe.instructions
            form.servings.data = recipe.servings
        else:
            form.name.data = recipe.name
            form.description.data = recipe.description
            form.category.data = recipe.category
            form.instructions.data = recipe.instructions
            form.servings.data = recipe.servings
    return render_template("update_recipe.html", form=form)

#region Delete Recipe
@recipe_routes.route("/delete-recipe/<rec_id>", methods=['GET', 'POST'])
@token_required
def delete_recipe(rec_id):
    form = DeleteRecipeForm()
    recipe = Recipe.query.get(rec_id)
    ing = Ingredients.query.filter_by(recipe_id=rec_id)
    if recipe is None:
        return render_template("error_404.html")
    else:
        if form.yes.data:
            if ing:
                for i in ing:
                    db.session.delete(i)
                    db.session.commit()
                db.session.delete(recipe)
                db.session.commit()
            else:
                db.session.delete(recipe)
                db.session.commit()
            return redirect(url_for('recipe_routes.recipes'))
        elif form.no.data:
            return redirect(url_for('recipe_routes.recipes'))
    return render_template("delete_recipe.html", form=form, recipe=recipe)

#region Search page
@recipe_routes.route("/search", methods=['GET', 'POST'])
def search():
    q = request.form.get('q')
    logged_in = is_logged_in()
    if q:
        results = Recipe.query.filter(Recipe.name.contains(q))
    else:
        results = []
    return render_template(
        "search.html", 
        results=results, 
        capitalize_title=capitalize_title,
        logged_in=logged_in
    )

#region Categories
@recipe_routes.route("/api/categories")
def api_category():
    categories = Categories.query.all()
    cat_list = []
    for cat in categories:
        cat_data = {'name': cat.name}
        cat_list.append(cat_data)
    return jsonify(cat_list)

@recipe_routes.route("/categories", methods=['GET'])
def categories():
    return render_template("categories.html")

#region Weekly Meal Plan
@recipe_routes.route("/meal-plan", methods=['POST', 'GET'])
@token_required
def get_meal_plan():
    breakfast, lunch, dinner = create_recipe_dicts()
    return render_template(
        "weekly_meal_plan.html", 
        breakfast=breakfast, 
        lunch=lunch, 
        dinner=dinner,
        capitalize_title=capitalize_title
    )