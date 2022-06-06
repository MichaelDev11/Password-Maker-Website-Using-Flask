#This was my first project using Flask, I learned what I did in this application from: https://www.youtube.com/watch?v=Z1RJmh_OqeA


from flask import Flask, redirect, render_template, request, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#class that will generate the contents of the table in the website.
class Generate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return ('<Password %r>' % self.id)

#posting the information
@app.route('/', methods=['POST', 'GET'])
def index():
    if (request.method == 'POST'):
        newpassword = str()
        length = 1
        incspec = request.form['includespecs']
        length = request.form['passwordLength']
        if (incspec.lower() == "y"):
            chars = "1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHKLZXCVBNM?"
            def split(chars):
                return [char for char in chars]
            characters = split(chars)
            for i in range(0, int(length)):
                newpassword += str(random.choice(characters))
            new_password = Generate(content=newpassword)
        else:
            chars = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHKLZXCVBNM"
            def split(chars):
                return [char for char in chars]
            characters = split(chars)
            for i in range(0, int(length)):
                newpassword += str(random.choice(characters))
            new_password = Generate(content=newpassword)
        try:
            db.session.add(new_password)
            db.session.commit()
            return redirect('/')
        except:
            return ("There was an issue generating your password")
    else:
        password = Generate.query.order_by(Generate.date_created).all()
        return(render_template('index.html', password=password))

@app.route('/delete/<int:id>')
def delete(id):
    password_to_delete = Generate.query.get_or_404(id)
    try:
        db.session.delete(password_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return ("There was a problem deleting that password")

if (__name__ == "__main__"):
    app.run(debug=True)
