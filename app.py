import os
import sqlite3
import requests
from flask import Flask, redirect, render_template, url_for, request, session, flash
from urllib.parse import urlencode
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = ''
CLIENT_SECRET = ''
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
REVOKE_URL = 'https://oauth2.googleapis.com/revoke'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

SCOPES = ['openid', 'profile', 'email']

def init_db():
    conn = sqlite3.connect('userss.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        google_id TEXT NOT NULL UNIQUE
    )''')
    conn.commit()
    conn.close()

init_db()  


@app.route('/login', methods = ['GET'])
def login():
    state = str(uuid.uuid4())
    session['oauth_state'] = state
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'state': state,
    }
    auth_url = f"{AUTHORIZATION_URL}?{urlencode(params)}"
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        flash('Invalid state parameter. Potential CSRF attack detected.')
        return redirect(url_for('index'))
   
    if not code:
        flash('Error: No code received.')
        return redirect(url_for('index'))
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(TOKEN_URL, data=data)
   
    if response.status_code != 200:
        flash(f'Error: Failed to get access token. {response.text}')
        return redirect(url_for('index'))
    token_data = response.json()
    access_token = token_data.get('access_token')

    if not access_token:
        flash('Error: No access token found.')
        return redirect(url_for('index'))

    user_info = get_user_info(access_token)
    session['user_info'] = user_info
    session['access_token'] = access_token

    return redirect(url_for('index'))


def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(USER_INFO_URL, headers=headers)
    if response.status_code != 200:
        flash(f'Error: Failed to fetch user information. {response.text}')
        return redirect(url_for('index'))

    user_info = response.json()
    add_or_update_user(user_info)

    return user_info



def add_or_update_user(user_info):
    conn = sqlite3.connect('userss.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE google_id = ?', (user_info['sub'],))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute('''UPDATE users SET name = ?, email = ? WHERE google_id = ?''',
                           (user_info['name'], user_info['email'], user_info['sub']))
        else:
            cursor.execute('''INSERT INTO users (name, email, google_id) VALUES (?, ?, ?)''',
                           (user_info['name'], user_info['email'], user_info['sub']))

        conn.commit()
    except Exception as e:
        print(f"Error during database operation: {e}")
    finally:
        conn.close()


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/explore')
def explore():
    return render_template('exploreArt.html')


@app.route('/about')
def about():
    return render_template('aboutus.html')


@app.route('/contact')
def contact():
    return render_template('formfinal.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/delete_account')
def delete_account():
    access_token = session.get('access_token')
    user_info = session.get('user_info')

    if not access_token or not user_info:
        flash('You are not logged in.')
        return redirect(url_for('index'))

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'token': access_token}
    response = requests.post(REVOKE_URL, data=data, headers=headers)

    if response.status_code == 200:
        delete_user(user_info['sub'])
        session.clear()
        flash('Your account has been deleted, and access has been revoked.')
    else:
        flash(f'Failed to revoke access. {response.text}')

    return redirect(url_for('index'))


def delete_user(google_id):
    conn = sqlite3.connect('userss.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM users WHERE google_id = ?', (google_id,))
    conn.commit()
    conn.close()


@app.route('/')
def index():
    if 'user_info' in session:  
        return render_template('index.html', user_name=session['user_info']['name'])
    else:
        return render_template('exploreArt.html')


if __name__ == '__main__':
    app.run(debug=True)
