from flask import Flask, send_from_directory, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html',
                               name=request.form['name'])
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                    'favicon.ico', mimetype='image/vnd.microsoft.icon')
