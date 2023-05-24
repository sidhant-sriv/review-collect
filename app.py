from flask import Flask, render_template, request, redirect
from scraper import get_rev, summarizer, question_answerer, get_product_review

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    url = None
    summary = None
    myrevs = []

    if request.method == 'POST':
        url = request.form['url']
        myrevs = get_rev(url)
        summary = summarizer(url)
    return render_template('summary.html', myrevs=myrevs, summary=summary)


@app.route('/qna', methods=['GET', 'POST'])
def qna():
    url = None
    answer = None
    question = None
    details = None
    if request.method == 'POST':
        url = request.form['url']
        question = request.form['question']
        details = get_product_review(url)
        print(details)
        answer = question_answerer(url, question)
    return render_template('qna.html', question=question, answer=answer, details=details)


if __name__ == '__main__':
    app.run()
