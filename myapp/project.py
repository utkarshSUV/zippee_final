from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/user/<username>')
def user_profile(username):
    return f'This is the profile page for {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'This is the page for post {post_id}'

if __name__ == '__main__':
    app.run()