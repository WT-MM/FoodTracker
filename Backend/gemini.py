import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image
from IPython.display import display
from IPython.display import Markdown

genai.configure(api_key="AIzaSyDLauzlSt5sqKyuWCvxSNmelNCVJRhC-Go")

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def name_foods(image):
    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(image)
    response = model.generate_content(["List all of the foods in this image and their shelf life formatted as a python dictionary where the food is the key and the expiration date is the value.", img], stream=True)
    response.resolve()
    print(response.text)

name_foods('Images/fridge.png')