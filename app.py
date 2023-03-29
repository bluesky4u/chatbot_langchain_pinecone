from flask import Flask, render_template, request, jsonify, redirect,send_from_directory
from chat import get_response_v3, OPENAI_API_KEY

from flask_cors import CORS
#from upload import upload




app=Flask(__name__)
CORS(app)

@app.get("/")
def index_get():
    return redirect("https://wordpress-924246-3356990.cloudwaysapps.com/", code=302)

@app.route('/loader')
def serve_loader_js():
    agent = request.args.get('agent', 'none')
    return send_from_directory('./', 'loader.js')

@app.get("/app")
def app_get():
    return render_template('base.html')

@app.post("/upload")
def upload():
    text=request.get_json().get("ticker")
    response = upload(ticker, OPENAI_API_KEY)
    message = {"answer": response}
    return jsonify(message)


@app.post("/predict")
def predict():
    agent=request.get_json().get("agent")
    query=request.get_json().get("message")
    response = get_response_v3(agent, query, OPENAI_API_KEY)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
    #app.run(host="localhost", port=8000, debug=True)