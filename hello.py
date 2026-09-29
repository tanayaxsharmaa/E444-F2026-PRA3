from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)


def is_uoft_email(email):
    return email is not None and 'utoronto' in email.lower()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        if is_uoft_email(form.email.data):
            return redirect(url_for('chatbot'))
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'),
                           email=session.get('email'),
                           current_time=datetime.now(timezone.utc))


@app.route('/chatbot')
def chatbot():
    if not is_uoft_email(session.get('email')):
        return redirect(url_for('index'))
    return render_template('chatbot.html', name=session.get('name'),
                           email=session.get('email'))


@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"].strip()
    lower = message.lower()

    if "my name is" in lower:
        start = lower.index("my name is") + len("my name is")
        chat_name = message[start:].strip(" .!")
        session["chat_name"] = chat_name
        reply = "Nice to meet you, {}!".format(chat_name)
    elif "what is my name" in lower:
        chat_name = session.get("chat_name")
        if chat_name:
            reply = "Your name is {}.".format(chat_name)
        else:
            reply = "I don't know your name yet. Tell me by saying 'My name is ...'."
    elif "hello" in lower:
        reply = "Hello!"
    else:
        reply = "I don't understand."

    return {"reply": reply}


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("What is your UofT email address?",
                        validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

if __name__ == '__main__':
    app.run(debug=True)
