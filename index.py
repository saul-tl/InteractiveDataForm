from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('nueva_publicacion.html')

@app.route('/add_post', methods=['GET','POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        data = {'title': title, 'body': body, 'userId': 1}
        response = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
        return jsonify(response.json()), response.status_code
    return render_template('nueva_publicacion.html')
@app.route('/display_get', methods=['GET'])
def display_get():
    title = request.args.get('title', 'No title Provided')
    body = request.args.get('body', 'No body Provided')
    return render_template('muestra_datos.html', title=title, body=body)

@app.route('/get_app', methods=['GET'])
def get_app():
   title = request.args.get('title')
   body = request.args.get('body')
   return render_template('muestra_datos.html', title=title, body=body)
if __name__ == "__main__":
    app.run(debug=True)