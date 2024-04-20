from flask import Flask, request, jsonify, render_template, redirect, session
import requests
import uuid

app = Flask(__name__)
app.secret_key = 'MLK6'  # Cambia esto por una clave secreta real

def generate_unique_id():
    return str(uuid.uuid4())  # Genera un UUID que es casi siempre único

@app.route('/')
def home():
    return render_template('nueva_publicacion.html')

@app.route('/muestra_datos', methods=['GET', 'POST'])
def muestra_datos():
    if 'local_posts' not in session:
        session['local_posts'] = []  # Inicializa la lista de publicaciones locales en la sesión si no existe

    if request.method == 'POST':
        new_post = {
            'title': request.form['title'],
            'body': request.form['body'],
            'id': generate_unique_id()  # Asigna un ID único a cada nueva publicación local
        }
        session['local_posts'].append(new_post)
        session.modified = True

    num_posts = request.args.get('num_posts', default=5, type=int)
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts?_limit={num_posts}')
    api_posts = response.json() if response.status_code == 200 else []

    posts = api_posts + session['local_posts']
    return render_template('muestra_datos.html', posts=posts)

@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Intenta encontrar la publicación en las publicaciones locales
    post = next((item for item in session.get('local_posts', []) if item['id'] == post_id), None)
    
    if not post:
        return "Publicación no encontrada", 404  # No se encontró la publicación, retorna un error 404

    if request.method == 'POST':
        # Actualiza la publicación con los datos del formulario
        post['title'] = request.form['title']
        post['body'] = request.form['body']
        session.modified = True  # Indica que la sesión ha sido modificada para guardar los cambios
        return redirect('/muestra_datos')

    return render_template('editar_publicaciones.html', post=post)


@app.route('/delete_post/<post_id>', methods=['GET'])
def delete_post(post_id):
    # Filtra la lista de publicaciones locales para eliminar la publicación con el ID especificado
    session['local_posts'] = [post for post in session.get('local_posts', []) if post['id'] != post_id]
    session.modified = True
    return redirect('/muestra_datos')


if __name__ == "__main__":
    app.run(debug=True)
