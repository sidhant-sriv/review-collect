from flask import Flask, render_template, request, redirect
from scraper import get_rev

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarizer', methods=['GET', 'POST'])
def home():
    url = None
    myrevs = []

    if request.method == 'POST':
        url = request.form['url']
        myrevs = get_rev(url)

    return render_template('form.html', myrevs=myrevs)




if __name__ == '__main__':
    app.run()
