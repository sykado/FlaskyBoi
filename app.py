from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for posts
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if title and description:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            post_id = len(posts)
            posts.append({
                "id": post_id,
                "title": title,
                "description": description,
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
        posts.pop(post_id)
        # Update remaining post IDs
        for i, post in enumerate(posts):
            post['id'] = i
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

