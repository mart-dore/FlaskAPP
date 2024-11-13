from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour CSRF

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    if form.validate_on_submit():
        # Traiter les données du formulaire ici
        return redirect(url_for('success'))
    return render_template('index.html')

@app.route('/success')
def success():
    return "Form successfully submitted!"

if __name__ == "__main__":
    app.run(debug=True)
