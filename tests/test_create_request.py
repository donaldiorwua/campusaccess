import json 
import tempfile

book = {
    "title": "intro to python",
    "pages": "300",
    "author": "mr-don"
}
        
with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as temp_file:
    json.dump(book, temp_file, indent=4)

with tempfile.TemporaryFile(mode="r+t", encoding="utf-8") as file:
    books = json.load(file)
assert temp_file == books