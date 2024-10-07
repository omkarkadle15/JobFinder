import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import requests
import json
import sys

# Add the parent directory of 'web' to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection parameters
db_params = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}


def get_db_connection():
    return psycopg2.connect(**db_params)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_script', methods=['POST'])
def run_script():
    script = request.form['script']
    if script == 'linkedin':
        try:
            position = request.form['position']
            experience = request.form['experience']
            location = request.form['location']
            search_query = f"{position} {experience} years experience {location}"

            from server.scraper.LinkedIn.main import main as linkedin_main
            posts = linkedin_main(search_query)
            return redirect(url_for('results', new_data=True, source='linkedin'))
        except ImportError as e:
            print(f"Error importing LinkedIn scraper: {e}")
            return "Error: LinkedIn scraper module not found", 500
    elif script == 'upwork':
        return redirect(url_for('results'))


@app.route('/results')
def results():
    new_data = request.args.get('new_data', False)
    conn = get_db_connection()
    cursor = conn.cursor()
    if new_data:
        cursor.execute("SELECT id, author, content, email, phone_number FROM posts ORDER BY id DESC LIMIT 10")
    else:
        cursor.execute("SELECT id, author, content, email, phone_number FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template('results.html', posts=posts, new_data=new_data)


def query_llama(prompt, post_content):
    url = os.getenv("LLAMA_API_URL")

    data = {
        "model": "llama3.1",
        "prompt": f"Based on the following LinkedIn post, {prompt}\n\nPost content: {post_content}",
        "stream": False
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = json.loads(response.text)
        return result['response']
    else:
        return f"Error: Unable to get a response from the Llama model. Status code: {response.status_code}"


@app.route('/query_post', methods=['POST'])
def query_post():
    data = request.get_json()
    post_id = data.get('post_id')
    query = data.get('query')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM posts WHERE id = %s", (post_id,))
    post_content = cursor.fetchone()
    conn.close()

    if post_content:
        post_content = post_content[0]
        response = query_llama(query, post_content)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'Post not found'}), 404

@app.route('/get_full_content/<int:post_id>')
def get_full_content(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM posts WHERE id = %s", (post_id,))
    content = cursor.fetchone()[0]
    conn.close()
    return jsonify({'content': content})

@app.route('/send_email', methods=['POST'])
def send_email():
    post_id = request.form['post-id']
    to = request.form['to']
    subject = request.form['subject']
    message = request.form['message']
    attachment = request.files['attachment'] if 'attachment' in request.files else None

    # Here you would implement your email sending logic
    # For example, using the Flask-Mail extension or the `smtplib` library

    # For demonstration purposes, we'll just print the email details
    print(f"Sending email for Post ID: {post_id}")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    if attachment:
        print(f"Attachment: {attachment.filename}")


    return jsonify({'message': 'Email sent successfully'})

if __name__ == '__main__':
    app.run(debug=True)