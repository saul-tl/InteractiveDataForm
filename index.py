from flask import Flask, redirect, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():    
    return render_template('nueva_publicacion.html')

@app.route('/muestra_datos')
def muestra_datos():
    # Obtener publicaciones de la API
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json() if response.status_code == 200 else []
    
    # Obtener datos enviados localmente, si existen
    title = request.args.get('title')
    body = request.args.get('body')
    if title and body:
        local_post = {'title': title, 'body': body, 'id': 0}  # ID 0 para identificar como local
        posts.append(local_post)

    return render_template('muestra_datos.html', posts=posts)



@app.route('/add_post', methods=['GET','POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        data = {'title': title, 'body': body, 'userId': 1}
        response = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
        if response.status_code == 201:  # Asumiendo que la publicación fue creada con éxito
            return redirect('/muestra_datos')
        else:
            return f"Error al crear publicación: {response.status_code}"
    return render_template('nueva_publicacion.html')


@app.route('/display_get', methods=['GET'])
def display_get():
    title = request.args.get('title', 'No title Provided')
    body = request.args.get('body', 'No body Provided')
    post = {'title':title, 'body':body}
    return render_template('muestra_datos.html', post=post)

@app.route('/get_app', methods=['GET'])
def get_app():
   title = request.args.get('title')
   body = request.args.get('body')
   return render_template('muestra_datos.html', title=title, body=body)

@app.route('/edit_post/<int:post_id>', methods=['GET'])
def edit_post(post_id):    
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}')
    if response.status_code == 200:
        post = response.json()
        return render_template('editar_publicacion.html', post=post)
    else:
        return f'Error al cargar la publicación: {response.status_code}'

   
@app.route('/edit_post/<int:post_id>', methods=['POST'])
def update_post(post_id):
    title = request.form['title']
    body = request.form['body']
    data = {'title': title, 'body': body}
    response = requests.put(f'https://jsonplaceholder.typicode.com/posts/{post_id}', json=data)
    if response.status_code == 200:
        return redirect('/muestra_datos')
    else:
        return f'Error al actualizar la publicación: {response.status_code}'
    
@app.route('/delete_post/<int:post_id>', methods=['GET'])
def delete_post(post_id):
   response = requests.delete(f'https://jsonplaceholder.typicode.com/posts/{post_id}')
   if response.status_code == 200:
       return redirect('/muestra_datos')
   else:
       return f'Error al eliminar la publicación: {response.status_code}'   

if __name__ == "__main__":
    app.run(debug=True)