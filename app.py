from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, send_file, abort
import os
import shutil

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Stronger Secret Key

# Dummy user credentials (Replace with database in real projects)
USER_CREDENTIALS = {"admin": "admin"}

# Define the directory where software files are stored
SOFTWARE_DIR = os.path.join(os.getcwd(), "software")
if not os.path.exists(SOFTWARE_DIR):
    os.makedirs(SOFTWARE_DIR)  # Create folder if it doesn't exist

# Security software keywords for classification
SECURITY_SOFTWARE_KEYWORDS = ["qualys", "crowdstrike", "bitdefender", "rapid 7", "kaspersky"]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['user'] = username  # Store user in session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/software')
def software():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get the list of available software files
    all_files = os.listdir(SOFTWARE_DIR) if os.path.exists(SOFTWARE_DIR) else []

    security_softwares = [file for file in all_files if any(keyword in file.lower() for keyword in SECURITY_SOFTWARE_KEYWORDS)]
    other_softwares = [file for file in all_files if file not in security_softwares]
    
    return render_template('Software.html', security_softwares=security_softwares, other_softwares=other_softwares)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(SOFTWARE_DIR, filename)

    if not os.path.exists(file_path):
        abort(404)  # Return 404 if file/folder doesn't exist

    if os.path.isdir(file_path):  # If it's a folder, zip it before downloading
        zip_path = f"{file_path}.zip"
        if not os.path.exists(zip_path):  # Create ZIP only if it doesn't already exist
            shutil.make_archive(file_path, 'zip', file_path)
        return send_file(zip_path, as_attachment=True)

    return send_from_directory(SOFTWARE_DIR, filename, as_attachment=True)

@app.route('/TeamMembers')
def team_members():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Team_Members.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
