from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

SezzleWebApp = Flask(__name__)
SezzleWebApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(SezzleWebApp)
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@SezzleWebApp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        calc = request.form['calculate']
        answer = eval(request.form['calculate'])
        full_calculation = str(calc) + " = " + str(answer)
        add_full_calc = Todo(content=full_calculation)

        try:
            db.session.add(add_full_calc)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue in task added'
    else:
        tasks = Todo.query.order_by(Todo.date_created.desc()).limit(10).all()
        return render_template('index.html', calculations=tasks)

@SezzleWebApp.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue with deleting task'

if __name__ == "__main__":
    SezzleWebApp.run(debug = True)