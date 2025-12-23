from recipe_app import db

class Ingredients(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient_name = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.String(255))

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    category = db.Column(db.String(), db.ForeignKey('categories.name'))
    ingredients = db.relationship('Ingredients', backref='recipe')
    instructions = db.Column(db.Text, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    
class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))