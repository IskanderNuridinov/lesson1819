from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        category_id = request.form['category_id']
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        status = request.form['status']
        new_task = Task(category_id=category_id, title=title, description=description, priority=priority, status=status)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    categories = Category.query.all()
    return render_template('add_task.html', categories=categories)

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    categorys = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_category.html', categorys=categorys)

@app.route('/category_list', methods=['GET', 'POST'])
def category_list():
    categorys = Category.query.all()
    return render_template('category_list.html', categorys=categorys)
    # return redirect(url_for('index'))
    # return render_template('category_list.html')

@app.route('/category_list/<int:category_id>', methods=['POST'])
def remove_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    # flash('Категория успешно удалена!', 'success')
    return redirect(url_for('category_list'))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()