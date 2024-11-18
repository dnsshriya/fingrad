# from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'

#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'

#     else:
#         return render_template('update.html', task=task)


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Sample in-memory task list
tasks = []

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/assignment', methods=['GET'])
def assignment_page():
    return render_template('assignment/index.html', tasks=tasks)

@app.route('/assignment', methods=['POST'])
def add_task():
    task_content = request.form.get('content')
    if task_content:
        tasks.append({'id': len(tasks) + 1, 'content': task_content, 'date_created': datetime.now()})
    return redirect(url_for('assignment_page'))

@app.route('/assignment/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('assignment_page'))

@app.route('/assignment/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content:
            task['content'] = task_content
        return redirect(url_for('assignment_page'))
    return render_template('assignment/update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
