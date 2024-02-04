import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image
from IPython.display import display
from IPython.display import Markdown
import json

genai.configure(api_key="AIzaSyDLauzlSt5sqKyuWCvxSNmelNCVJRhC-Go")
modelV = genai.GenerativeModel('gemini-pro-vision')
modelT = genai.GenerativeModel('gemini-pro')

with open("./ModifiedNames.txt", "r") as file:
    data = file.read()
    data = data.split("\n")
    data = ', '.join(data)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def name_foods(image):
    img = PIL.Image.open(image)
    response = modelV.generate_content(['''Return all of the foods in this image and their associated expiration date.
                                       Put the dates in yyyy-mm-dd format.
                                       Assume the current day is February 4, 2024.
                                       Format the entire answer as [{"name": 'food', "date": 'date'}, {"name": 'food', "date": 'date'}''', img], stream=True)
    response.resolve()
    mydict = json.loads(response.text)
    return mydict


def get_recipe(foods):
    foodString = ', '.join(foods)
    response = modelT.generate_content(f'''Return possible recipes from the following foods: {foodString}"]
                                          Do not give the ingredients, just the names of the recipes.
                                          Give at most 5 recipes.
                                          Format the entire answer as 'recipe1, recipe2, recipe3' without any enumeration''', stream=True)
    response.resolve()
    return response.text.split(", ")
