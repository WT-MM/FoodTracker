import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image
from IPython.display import display
from IPython.display import Markdown

genai.configure(api_key="AIzaSyDLauzlSt5sqKyuWCvxSNmelNCVJRhC-Go")

with open("./ModifiedNames.txt", "r") as file:
    data = file.read()
    data = data.split("\n")
    data = ', '.join(data)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def name_foods(image):
    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(image)
    response = model.generate_content(["Return all of the foods in this image in a single string separated by commas that are also in the following list: " + data, img], stream=True)
    response.resolve()
    print(response.text)
