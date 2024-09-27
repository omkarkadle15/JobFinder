from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import psycopg2
import requests
import json

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(database="linkedin", user="postgres", password="postgres", host="localhost", port="5432")
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    script = request.form['script']
    if script == 'linkedin':
        subprocess.run(['python', 'JobFinder/server/scraper/LinkedIn/main.py'])
    elif script == 'upwork':
        subprocess.run(['python', 'JobFinder/server/scraper/Upwork/scraper.py'])
    return redirect(url_for('results'))

@app.route('/results')
def results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, author, content FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return render_template('results.html', posts=posts)

def query_llama(prompt, post_content):
    url = "http://localhost:11434/api/generate"
    
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

    if post_content:
        post_content = post_content[0]
        response = query_llama(query, post_content)
        return jsonify({'response': response})
    else:
        return jsonify({'response': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)