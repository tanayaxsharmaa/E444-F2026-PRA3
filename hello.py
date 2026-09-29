from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template('index.html', form=form, name=name,
                           current_time=datetime.now(timezone.utc))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

if __name__ == '__main__':
    app.run(debug=True)
