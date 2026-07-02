import re, os
from flask import flash
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from openai import (AuthenticationError, APITimeoutError, APIConnectionError, 
                    BadRequestError, RateLimitError, InternalServerError)
from typing import List, Union
from recipe_app.pdfreader.shared import parse_ingredients

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class RecipeData(BaseModel):
    name: str = Field(description="The name of the recipe. Can usually be found in the very first chunk.")
    description: str = Field(description="Describes the recipe.")
    category: str | None = Field(description="Based on the name of the recipe, the value could be only one of the following types: breakfast, lunch, dinner, appetizer, or dessert. If unclear set to None.")
    ingredients: List[str] = Field(description="The ingredients found in the list. Look for the quantity and name of the ingredient.")
    instructions: str = Field(description="The instructions of the recipe found in list. Any line that appears to be a guide to making the recipe.")

OPEN_AI_MODEL = "gpt-4.1-nano"

class LLMClient():
    def __init__(self, model, temperature, chunks):
        self.model = model
        self.temperature = temperature
        self.chunks = chunks

    def create_agent(self):
        try:
            agent = ChatOpenAI(model=self.model, temperature=self.temperature, api_key=OPENAI_API_KEY)
        except Exception as e:
            flash(f"Failed to create model: {type(e)} {e}", "error")

        return agent

    def invoke_agent(self):
        agent = self.create_agent()
        if agent:
            structured_agent = agent.with_structured_output(RecipeData)
            prompt = f"You are a helpful assistant that extracts recipe information from text. You will be given a list called chunks: {self.chunks}. " \
            "Each list inside chunk contains strings of lines, and you will extract the description, category, ingredients, and " \
            "instructions. You will return the information in a structured format."
            results = structured_agent.invoke(prompt)
            return results
        
    def find_nearest_int(self, line: str) -> str:
        # find index with servings. split list into left and right portion
        # find nearest int in left and right portion. if both are the same distance, return the larger one. 
        # if one is closer than the other, return that one.
        servings = r"servings"
        # find if servings is in line. if it is, find the index of servings. split the line into left and right portion. find the nearest int in left and right portion. if both are the same distance, return the larger one. if one is closer than the other, return that one.
        for word in line:
            if len(line) > 1:
                if re.search(servings, word):
                    index = line.index(word)
                    left_portion = line[:index]
                    right_portion = line[index+1:]
                    if left_portion and right_portion:
                        clever = zip(left_portion[::-1], right_portion)
                        nearest_int = None
                        for left_word, right_word in clever:
                            if left_word.isdigit() and not right_word.isdigit():
                                nearest_int = left_word
                                break
                            if right_word.isdigit() and not left_word.isdigit():
                                nearest_int = right_word
                                break
                            if left_word.isdigit() and right_word.isdigit():
                                nearest_int = right_word
                                break
                    elif not left_portion and right_portion:
                        for word in right_portion:
                            if word.isdigit():
                                nearest_int = word
                                break
                    elif left_portion and not right_portion:
                        for word in left_portion[::-1]:
                            if word.isdigit():
                                nearest_int = word
                                break

                    return nearest_int
    
    def find_recipe_servings(self, chunks: list):
        for chunk in chunks:
            for line in chunk:
                if "servings" in line.lower():
                    line = line.lower().split()
                    servings = self.find_nearest_int(line)
                    return servings
        
    def autofill_data(self, form):
        try:
            results = self.invoke_agent()
            servings = self.find_recipe_servings(self.chunks)
            ing_list = []
            
            for line in results.ingredients:
                parsed_ingredient = parse_ingredients(line)
                ing_list.append(parsed_ingredient)

            form.name.data = results.name
            form.description.data = results.description
            form.category.data = results.category
            form.servings.data = servings

            form.ingredients.pop_entry()
            for ings in ing_list:
                form.ingredients.append_entry(ings)
            
            form.instructions.data = results.instructions
        except AuthenticationError as e:
            flash(f"Invalid, expired, or revoked API key.", "error")
        except APIConnectionError as e:
            flash(f"Network connection failure. Please check your network settings, proxy, or firewall.", "error")
        except APITimeoutError as e:
            flash(f"API request timed out. Please try again later.", "error")
        except RateLimitError as e:
            if e.code == "insufficient_quota":
                flash("Error: insufficient credits. Tell that boy to put more money in his OpenAI account!", "error")
            else:
                flash(f"Rate limit error. Too many requests being made at once.", "error")
        except BadRequestError as e:
            flash(f"Bad request error: {e}", "error")
        except InternalServerError as e:
            flash(f"Server side error. Something gone bad on OpenAI's side. Try again later.", "error")