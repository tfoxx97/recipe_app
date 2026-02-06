from flask_wtf import FlaskForm, Form
from wtforms import (FormField, StringField, IntegerField, 
                     SubmitField, FieldList, SelectField)
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from recipe_app.utils import getCategories

# inherits from Form because of missing csrf token issue
class IngredientsForm(Form):
    ing_name = StringField('Ingredient')
    quantity = StringField('Quantity')

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = CKEditorField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=getCategories)
    ingredients = FieldList(FormField(IngredientsForm, 'Ingredients'), min_entries=1, max_entries=50)
    servings = IntegerField('Servings', validators=[DataRequired()])
    instructions = CKEditorField('Instructions', validators=[DataRequired()])
    create_recipe = SubmitField('Create Recipe')
    add_ing = SubmitField('Add Ingredient')
    del_ing = SubmitField('Delete Ingredient', render_kw={"disabled": True})

class DeleteRecipeForm(FlaskForm):
    yes = SubmitField('Yes')
    no = SubmitField('No')