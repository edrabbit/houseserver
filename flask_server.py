import flask
import requests

import my_settings as settings


app = flask.Flask(__name__)

AUTH = requests.auth.HTTPDigestAuth(settings.INDIGO_USER, settings.INDIGO_PASS)


def _get_variable_value(variable):
    uri = settings.INDIGO_URI_VAR + variable + '.json'
    r = requests.get(uri, auth=AUTH)
    return r.json()['value']


def _set_variable_value(variable, value):
    uri = ("%s%s?_method=put&value=%s"
           % (settings.INDIGO_URI_VAR, variable, value))
    r = requests.get(uri, auth=AUTH)
    if r.status_code == 200:
        return True
    else:
        return False


def fetch_cat_bathroom_score():
    cb_score = _get_variable_value('cat_bathroom_score')
    return cb_score


def reset_cat_bathroom_score():
    return _set_variable_value('cat_bathroom_score', '0')


@app.route("/")
def root():
    return flask.render_template('index.html')


def display_cat_bathroom(values={}):
    values['score'] = fetch_cat_bathroom_score()
    return flask.render_template(
        'catbathroom.html', values=values, title="Cat Bathroom")


@app.route('/catbathroom')
@app.route('/catbathroom/')
@app.route('/catbathroom/<action>')
def cat_bathroom(action=None):
    if not action:
        return display_cat_bathroom()
    else:
        if action == "reset":
            successful = reset_cat_bathroom_score()
            return flask.redirect(flask.url_for('cat_bathroom'))
        else:
            return "Unsupported action: %s" % action

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
