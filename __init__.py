from app_config import app, port
from controller import blue_prints

for bp in blue_prints:
    app.register_blueprint(bp[0], url_prefix=bp[1])


@app.route('/')
@app.route('/index')
def index():
    return 'helloworld'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
