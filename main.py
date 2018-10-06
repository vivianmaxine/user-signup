from flask import Flask, redirect, request
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

# Displays user sign-up page


@app.route('/', methods=['GET'])
def display_form():
    template = jinja_env.get_template('user-signup.html')
    return template.render()


# Processes user sign-up page


@app.route('/', methods=['POST'])
def validate_form():
    user_name = request.form['user_name']
    user_pw = request.form['user_pw']
    user_pw_verify = request.form['user_pw_verify']
    user_email = request.form['user_email']

    name_error = ''
    pw_error = ''
    pw_verify_error = ''
    email_error = ''

    # Username field
    if user_name == '':
        name_error = "Please enter your name."
    else:
        if ' ' in user_name:
            name_error = "Please remove any spaces from your name."
        else:
            if len(user_name) < 2 or len(user_name) > 20:
                name_error = "First name must be 2-20 characters long."

    # Password field
    if user_pw == '':
        pw_error = "Please enter a password."

    if 3 <= len(user_pw) <= 20:
        if ' ' in user_pw:
            pw_error = 'Passwords should have no spaces.'
    else:
        pw_error = "Password must be 3-20 characters long."

    # Password verify field
    if pw_error == '' and user_pw != user_pw_verify:
        pw_verify_error = "Make sure your passwords match."

    if user_pw_verify == '':
        pw_verify_error = 'Please verify your password.'

    # Email field
    if user_email != '':
        if len(user_email) >= 3 and len(user_email) <= 20:
            if '@' in user_email and '.' in user_email:
                if ' ' in user_email:
                    email_error = "Email addresses should not have any spaces."
            else:
                email_error = "Use proper email formatting."
        else:
            email_error = "Email addresses must be 3-20 characters long."

    # Confirm information and redirect to welcome page
    if not any([name_error, pw_error, pw_verify_error, email_error]):
        return redirect('/welcome?user_name={0}'.format(user_name))

    template = jinja_env.get_template('user-signup.html')
    return template.render(
        user_name=user_name,
        name_error=name_error,
        user_pw=user_pw,
        pw_error=pw_error,
        user_pw_verify=user_pw_verify,
        pw_verify_error=pw_verify_error,
        user_email=user_email,
        email_error=email_error)


# Processes user welcome page


@app.route('/welcome', methods=['GET'])  # redirect is get method
def welcome_message():
    user_name = request.args.get('user_name')

    template = jinja_env.get_template('welcome.html')
    return template.render(
        user_name=user_name)

app.run()
