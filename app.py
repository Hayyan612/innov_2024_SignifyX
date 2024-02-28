from flask import Flask, render_template, request, redirect, url_for, session
from main import helper, get_popular, get_now_playing

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    pop_list = get_popular()
    now_list = get_now_playing()
    return render_template('index.html', pop_list=pop_list, now_list=now_list)
    

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/joinus.html')
def joinus():
    return render_template('joinus.html')

@app.route('/review.html')
def review():
    return render_template('review.html')

@app.route('/single.html')
def single():
    return render_template('single.html')
@app.route('/anime-main/login.html')
def login():
    return render_template('anime-main/login.html')

@app.route('/select', methods=['POST', 'GET'])
def select():
    value = request.form['operator']
    print(value)
    x = helper(value)
    print(x)
    return render_template('review.html', x=x, value=value)
    

if __name__ == '__main__':
    app.run(debug=True)