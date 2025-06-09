from flask import Flask, render_template, request, redirect, url_for
import json
import os


app = Flask(__name__)


def load_posts():
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def get_next_id(posts):
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()

        new_post = {
            "id": get_next_id(blog_posts),
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        blog_posts.append(new_post)

        with open("blog_posts.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)