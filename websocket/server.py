from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello_again')
def hello_world_again():
    return 'Hello again, World!'

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         return render_template('index.html',
#                                name=request.form['name'])
#     return render_template('index.html')


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                     'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
