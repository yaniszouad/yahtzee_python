from flask import request

def login():
    #returning a dictionary automatically sends json
    # curl "http://127.0.0.1:5000"   
    print(f"request.url={request.url}")
    return {
        "message":"Hello servers with Python Flask"
    }