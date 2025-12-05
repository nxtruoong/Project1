from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    finished = db.Column(db.Boolean, default=False)
    date_finished = db.Column(db.DateTime, nullable=True)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding your task'
    else:
        tasks = Todo.query.filter(Todo.finished == False).order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks) 

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') 
    except:
        return 'There was an error in deleting your task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a error updating your task'
    else: 
        return render_template('update.html', task = task_to_update)

@app.route('/finish/<int:id>', methods=['POST'])
def finish(id): 
    task_to_finish = Todo.query.get_or_404(id)

    try:
        task_to_finish.finished = True
        task_to_finish.date_finished = datetime.utcnow()
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a error checking "finished" for your task'

@app.route('/archive/', methods=['GET'])
def archive():
    tasks_finished = Todo.query.filter(Todo.finished == True).order_by(Todo.date_finished.desc()).all()
    return render_template('archive_finished.html', tasks = tasks_finished)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


