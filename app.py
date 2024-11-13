from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour CSRF

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit form')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    if form.validate_on_submit():
        # Traiter les données du formulaire ici
        return render_template('name.html', name = form.name.data)
    return render_template('index.html',
                           form=form)

@app.route('/success')
def success():
    return "Form successfully submitted!"

# ERRORS

# Invalid URL / Pagename
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Servor Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)


