from flask import jsonify
from flask import request

def hello():
    #Getting information via the query string portion of a URL
    # curl "http://127.0.0.1:5000/fruit/"
    # curl "http://127.0.0.1:5000/fruit?index=0"

    print(f"request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('index')}")
    
    fruit = ["oranges", "apples", "blueberries"]
    if request.args.get('index'):
        index = int(request.args.get('index'))

        if index >= 0 and index <len(fruit):
            return jsonify(fruit[index]) 
        else:
            return jsonify([])
    else:
        # lists are techincally valid json
        return jsonify(fruit)

def fruit_tips(fruit_name):
    #Getting information via the path portion of a URL
    print(f"request.url={request.url}")
    food={
    "oranges": "https://en.wikipedia.org/wiki/Orange_(fruit)",
    "apples": "https://en.wikipedia.org/wiki/Apple",
    "blueberries": "https://en.wikipedia.org/wiki/Blueberry"
    }
    if request.method == 'GET':
        # curl "http://127.0.0.1:5000/fruit/apples"
        if fruit_name in food:
            return {
                fruit_name:food[fruit_name]
                }
        else:
            return {}
    elif request.method == 'POST':
        #curl -X POST -H "Content-type: application/json" -d '{ "name" : "tomatoes", "url":"https://en.wikipedia.org/wiki/Tomato"}' "http://127.0.0.1:5000/fruit/new"
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
           # or request.is_json:
            data = request.json
            food[data["name"]] = data["url"]
            return food
        else:
            return {}
            