from flask import Flask, render_template,request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# clearing warnigs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True#False
#initialising the  database

db = SQLAlchemy(app)



# Creating Modules
# clases are used to create database tables

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)


    # repr define how 1 obj would be represented

    def __repr__(self):
        return f"Name: {self.fname}, Age: {self.age}"
     




@app.route('/', methods=['GET'])

# Fetching all users
def index():
    users = Users.query.all() # all database entries
    print("Fetching Users ")
    print(f" Users: {users}")
    return render_template('index.html', users=users)



# Adding new User
@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    return render_template('add_user.html'), 200 #   Present the User Add page to Users


# Endpoint for User Creation
@app.route('/register', methods=['POST'])
def register():
    # fname = requests.get('fname')
    user_data = request.form # Data from input Forms

    fname = user_data.get('fname')
    lname = user_data.get('lname')
    age  = user_data.get('age')

    if fname != '' and lname != '' and age != None:
        user = Users(fname=fname, lname=lname, age=age)
        db.session.add(user)
        db.session.commit()
        #flash('User Added SuccessFully', 'green')
        print("Entries Added Successfully")
        return redirect(url_for('index'))
    else:
        #flash('Error Occured During Process', 'red')
        print("An Error Occured during Registration")
        return redirect(url_for('index'))


# Delete User in DB
@app.route('/delete/<int:id>') # if left as str alchemy auto corrects it
def delete(id):
    print(f"TYPE of ID: {type(id)}")
    data = Users.query.get(id)
    print(f'Details: {data}, {type(data)}')
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == "__main__":
    with app.app_context(): # Ensuring all db initialisation is working well
        db.create_all() # creating datases
    
    app.run(debug=True)