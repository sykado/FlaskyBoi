from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import zipfile
import io

app = Flask(__name__)

# In-memory storage for posts
posts = []

UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('zipfile')
        
        if title and description and file and file.filename.endswith('.zip'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            post_id = len(posts)
            posts.append({
                "id": post_id,
                "title": title,
                "description": description,
                "filename": filename,
                "timestamp": timestamp
            })
            return redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 0 <= post_id < len(posts):
        post = posts[post_id]
        if request.method == 'POST':
            post['title'] = request.form.get('title')
            post['description'] = request.form.get('description')
            return redirect(url_for('index'))
        return render_template('edit_post.html', post=post)
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    if 0 <= post_id < len(posts):
        deleted_post = posts.pop(post_id)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], deleted_post['filename']))
        # Update remaining post IDs
        for i, post in enumerate(posts):
            post['id'] = i
    return redirect(url_for('index'))

@app.route('/download/<int:post_id>')
def download_file(post_id):
    if 0 <= post_id < len(posts):
        post = posts[post_id]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], post['filename'])
        return send_file(filepath, as_attachment=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

