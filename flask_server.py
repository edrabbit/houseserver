import flask


app = flask.Flask(__name__)


@app.route("/")
def hello():
    return "Hello flask world!"

def display_cat_bathroom():
    return flask.render_template('catbathroom.html')
#    return "<html><head><title>Cat Bathroom</title></head><body><h1>Cat Bathroom</h1></body></html>"

@app.route('/catbathroom')
@app.route('/catbathroom/')
@app.route('/catbathroom/<action>')
def cat_bathroom(action=None):
    if not action:
        return display_cat_bathroom()
    else:
        return "We are performing %s on cat bathroom" % action

if __name__ == "__main__":
    app.debug = True
    #app.config['SERVERNAME'] = 'localhost:80'
    app.run(host='0.0.0.0', port=8080)

