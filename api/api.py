import time
from flask import Flask, request, jsonify
import sys

sys.path.insert(1, './model/src')
from generate_translations import translate


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def hello():
    return jsonify("hello") 

@app.route('/translate', methods=['POST'])
def json_example():
    request_data = request.get_json()
    try:
        source = request_data['source_sentence']
        source_capitalized = source[0].upper() + source[1:]
        translations = translate(source_capitalized)
        return jsonify(translations)
    except:
        error = {"error": "An error occurred translating sentences :("}
        return jsonify(error)  
    
if __name__ == "__main__":
    app.run(port=8000, debug=True)