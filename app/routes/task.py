from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from app import db
from sqlalchemy import delete
from app.models import Task

# Blueprint is named 'tasks'
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    
    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)

@task_bp.route('/add', methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')

    # 🚨 FIX 2: Changed 'task.view_tasks' to 'tasks.view_tasks'
    return redirect(url_for('tasks.view_tasks'))

@task_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    # 🚨 FIX 3: Added login check
    if 'user' not in session:
        return redirect(url_for("auth.login"))
        
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working' # 🚨 FIX 1: Changed == to =
        elif task.status == 'Working':
            task.status = 'Done'    # 🚨 FIX 1: Changed == to =
        else:
            task.status = 'Pending' # 🚨 FIX 1: Changed == to =
        db.session.commit()
    
    # This redirect was already correct for the Blueprint name 'tasks'
    return redirect(url_for('tasks.view_tasks'))

@task_bp.route('/clear', methods=["POST"])
def clear_tasks():
    # 🚨 FIX 3: Added login check
    if 'user' not in session:
        return redirect(url_for("auth.login"))
        
    # Assuming Task.query.delete() is a valid SQLAlchemy-specific method for the ORM version you are using
    Task.query.delete(synchronize_session='fetch')
    db.session.commit()
    flash('All tasks cleared !', 'info')
    
    # This redirect was already correct for the Blueprint name 'tasks'
    return redirect(url_for('tasks.view_tasks'))