from flask import Flask, render_template
import json
import os


app = Flask(__name__)



def load_posts():
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r") as file:
            return json.load(file)
    return []


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)