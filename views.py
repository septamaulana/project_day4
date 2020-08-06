from flask import abort, request, render_template, redirect, url_for, \
    session, flash
from app import app, db
from forms import RegisterForm, LoginForm, TaskForm, DeleteForm
from models import User, Task
from auth import login_required

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        field_username = form.username.data
        field_password = form.password.data
        existing_username = User.query.filter_by(username=field_username).first()

        if not existing_username:
            user = User(field_username, field_password)
            db.session.add(user)
            db.session.commit()
            flash('You are now registered. Please login')
            return redirect(url_for('login'))
        else:
            flash('Username already have!')
    elif form.errors:
        flash('Form not Valid!')
    return render_template('register.html', form=form, title="Register | TodoApp")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        field_username = form.username.data
        field_password = form.password.data
        get_user = User.query.filter_by(username=field_username).first()
        if get_user and get_user.check_password(field_password):
            flash('Login Success!')
            session["username"] = field_username
            return redirect(url_for('index'))
        else:
            flash('Login Failed! Wrong Password')
    return render_template('login.html', form=form, title='Login | TodoApp')

@app.route('/')
@login_required
def index(*args, **kwargs):
    user = kwargs.get('user')
    return render_template('index.html', user=user, title="Home | ToDoApp")

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        flash('You have successfully logged out.')
    return redirect(url_for('login'))

@app.route('/todos/add', methods=['GET', 'POST'])
@login_required
def todo_add(*args, **kwargs):
    user = kwargs.get('user')
    form=TaskForm()
    if form.validate_on_submit():
        field_content = form.content.data
        field_status = int(form.status.data)
        task = Task(content=field_content, status=field_status, user_id=user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task has been added!')
        return redirect(url_for('todo_list'))
    return render_template('todo/add.html', form=form, title="Add Task | TodoApp")

@app.route('/todos')
@login_required
def todo_list(*args, **kwargs):
    user = kwargs.get('user')
    task_list = Task.query.filter_by(user_id=user.id).all()
    return render_template('todo/list.html', data_list=task_list, title="Ta Do List | TodoApp")

@app.route('/todos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def todo_edit(*args, **kwargs):
    user = kwargs.get('user')
    id = kwargs.get('id')
    current_task = Task.query.get_or_404(id)
    form = TaskForm(
        content=current_task.content,
        status=current_task.status
)
    if form.validate_on_submit():
        current_task.content = form.content.data
        current_task.status = form.status.data
        db.session.add(current_task)
        db.session.commit()
        flash('Your Task has been updated!')
        return redirect(url_for('todo_list'))
    return render_template('todo/add.html', form=form, title='Edit Task | TodoApp')

@app.route('/todos/delete/<int:id>', methods=['GET','POST'])
def todo_delete(*args, **kwargs):
    id = kwargs.get('id')
    current_task = Task.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(current_task)
        db.session.commit()
        flash('Your Task has been deleted!')
        return redirect(url_for('todo_list'))

    return render_template('todo/del.html', form=form, title='Delete Task | TodoApp')