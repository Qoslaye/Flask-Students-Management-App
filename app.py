from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'  # Corrected configuration key and file name
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)  # Corrected class name

class Students(db.Model):  # Corrected class name and capitalization
    id = db.Column('student_id', db.Integer, primary_key=True)  # Corrected column spelling and type
    name = db.Column(db.String(100))  # Corrected column type and spelling
    city = db.Column(db.String(50))  # Corrected column type and spelling
    addr = db.Column(db.String(200))  # Corrected column type and spelling
    pin = db.Column(db.String(10))  # Corrected column type and spelling

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

@app.route('/')
def show_all():
    return render_template('show_all.html', students=Students.query.all())  # Corrected template rendering

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(
                request.form['name'],
                request.form['city'],
                request.form['addr'],
                request.form['pin']
            )
            db.session.add(student)
            db.session.commit()  # Fixed typo in commit
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created within the application context
    app.run(debug=True)
