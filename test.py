from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form): #we define the class of the objects we will use in the form
    ville = TextField('Localisation (quelle ville ?) ', validators=[validators.required()])
    km = TextField('Localisation (dans un rayon de combien de km ?) ', validators=[validators.required()])
    keywords = TextField('Mots clés', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST': #when the person will try to send his form
        ville=request.form['ville']
        keywords=request.form['keywords']
        km=request.form['km']
        print ville, " ", km, " ", keywords
 
        if form.validate():
            # Save the comment here.
            flash('Nous lançons la recherche ...')
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('index.html', form=form) #it will send back the website
 
if __name__ == "__main__":
    app.run()