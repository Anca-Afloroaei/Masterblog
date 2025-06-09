from flask import Flask, render_template, request, redirect, url_for
import json
import os


app = Flask(__name__)

DATA_FILE = "blog_posts.json"

def load_posts():
    """
    Loading blog posts from JSON file
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def fetch_post_by_id(post_id):
    """
    Helper function to fetch a single post by ID
    """
    blog_posts = load_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None

# def get_next_id(posts):
#     if not posts:
#         return 1
#     return max(post["id"] for post in posts) + 1


@app.route('/')
def index():
    """
    Home route - index page showing all blog posts
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add route - displays form and handle new post creation
    """
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_posts()

        new_id = max([post["id"] for post in blog_posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Delete route - removes a post by ID
    """
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update route - displays form to update an existing post
    """
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        if request.method == 'POST':
            post['author'] = request.form.get('author')
            post['title'] = request.form.get('title')
            post['content'] = request.form.get('content')

            # Save the updated posts list
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(blog_posts, file, ensure_ascii=False, indent=4)

            return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """
    Like Route - allow the options to 'Like' a post and counts the number of 'Likes'
    """
    blog_posts = load_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    """
    Running the app
    """
    app.run(host="0.0.0.0", port=5001, debug=True)