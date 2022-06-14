import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template('index.html')


@app.route('/guide')
def load_guide_page():
    return flask.render_template('guide.html')


@app.route('/guide/<int:step>')
def load_guide_step(step):
    if step == 0:
        page_name = 'guide.html'
    else:
        page_name = f'guide_{step}.html'
    return flask.render_template(page_name)

@app.route('/graph')
def load_graph():
    return flask.render_template('graph.html')

if __name__ == '__main__':
    app.run()
