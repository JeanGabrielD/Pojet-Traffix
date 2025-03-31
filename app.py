from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Dummy user credentials
USER_CREDENTIALS = {
    'admin': 'password123',
    'user': 'mypassword'
}

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('pretraitement'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/algo-1', methods=['GET', 'POST'])
def algo1():

    return render_template('algo-1.html')

@app.route('/entrainement', methods=['GET', 'POST'])
def entrainement():

    return render_template('entrainement.html')

@app.route('/pretraitement', methods=['GET', 'POST'])
def pretraitement():

    return render_template('pretraitement.html')

@app.route('/visualisations', methods=['GET', 'POST'])
def visualisations():

    return render_template('visualisations.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)