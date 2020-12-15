import datetime
import iso8601

import flask
import requests

import my_settings as settings


app = flask.Flask(__name__)

AUTH = requests.auth.HTTPDigestAuth(settings.INDIGO_USER, settings.INDIGO_PASS)


def _get_variable_value(variable):
    uri = settings.INDIGO_URI_VAR + variable + '.json'
    print "about to get %s" % uri
    r = requests.get(uri, auth=AUTH)
    print r
    try:
        return r.json()['value']
    except ValueError:
        return "Not Found"


def _set_variable_value(variable, value):
    uri = ("%s%s?_method=put&value=%s"
           % (settings.INDIGO_URI_VAR, variable, value))
    r = requests.get(uri, auth=AUTH)
    if r.status_code == 200:
        return True
    else:
        return False


def fetch_first_time_ask_score():
    fta_score = _get_variable_value('first_time_ask_score')
    return fta_score

def reset_first_time_ask_score():
    print "in reset_first_time_ask_score"
    now = datetime.datetime.now()
    _set_variable_value('first_time_ask_last_reset', now.isoformat())
    _set_variable_value('first_time_ask_score', '0')

def fetch_last_fta_reset(dt=True):
    # returns datetime object with datetime of last reset
    first_time_ask_last_reset = _get_variable_value('first_time_ask_last_reset')
    if dt:
        last_reset_dt = iso8601.parse_date(first_time_ask_last_reset)
        return last_reset_dt
    else:
        return first_time_ask_last_reset

def fetch_cat_bathroom_score():
    cb_score = _get_variable_value('cat_bathroom_score')
    return cb_score

def fetch_last_cat_cleaning(dt=True):
    # returns datetime object with datetime of last cleaning
    last_cleaning = _get_variable_value('cat_last_cleaning')
    if dt:
        last_cleaning_dt = iso8601.parse_date(last_cleaning)
        return last_cleaning_dt
    else:
        return last_cleaning

def reset_cat_bathroom_score():
    now = datetime.datetime.now()
    _set_variable_value('cat_last_cleaning', now.isoformat())
    _set_variable_value('cat_bathroom_score', '0')


@app.route("/")
def root():
    return flask.render_template('index.html')

def display_cat_bathroom(values={}):
    values['score'] = fetch_cat_bathroom_score()

    last_cleaning = fetch_last_cat_cleaning(dt=True)
    values['last_date'] = (
        last_cleaning.isoformat().replace("T", " ").split('.')[0])

    today = datetime.datetime.now()
    values['days_since'] = (today.date() - last_cleaning.date()).days

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
            reset_cat_bathroom_score()
            return flask.redirect(flask.url_for('cat_bathroom'))
        else:
            return "Unsupported action: %s" % action

def display_fta(values={}):
    print "In display_fta"
    values['score'] = fetch_first_time_ask_score()
    print "score fetched"
    last_reset = fetch_last_fta_reset(dt=True)
    print "last_reset fetched"
    values['last_date'] = (
        last_reset.isoformat().replace("T", " ").split('.')[0])

    today = datetime.datetime.now()
    values['days_since'] = (today.date() - last_reset.date()).days

    colors = [
        "black",
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet"
    ]

    r = int(values['score'] / 10)
    values['color'] = colors[r]
    print "color should be %s" % values['color']
    return flask.render_template(
        'fta.html', values=values, title="First Time Ask")


@app.route('/fta')
@app.route('/fta/')
@app.route('/fta/<action>')
def fta(action=None):
    print "FTA"
    if not action:
        return display_fta()
    else:
        if action == "reset":
            reset_first_time_ask_score()
            return flask.redirect(flask.url_for('fta'))
        else:
            return "Unsupported action: %s" % action


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
