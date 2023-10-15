from flask import Flask, render_template,request,session,redirect,url_for

app = Flask(__name__)

app.secret_key = 'Claudia13'

usuarios = {'andres':'41662431','yovana':'41662431'}

@app.route('/login',methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in usuarios and usuarios[username] == password:
        session['username'] = username
        return redirect(url_for('main'))
    else:
        # Autenticación fallida, puedes mostrar un mensaje de error
        return render_template('index.html', error='Credenciales incorrectas')
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    if 'username' in session:
        
        return render_template('main.html')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)