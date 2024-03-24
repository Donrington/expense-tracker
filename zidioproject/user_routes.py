import json, os
from os.path import basename
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, extract
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from flask import *
from flask_socketio import SocketIO, emit, join_room, leave_room
from markupsafe import escape
import re
from flask_wtf.csrf import CSRFProtect
from zidioproject import app, csrf, socketio
from zidioproject.forms import *
from flask_login import login_required
from zidioproject.models import db, Expense, User
from zidioproject import mail
from flask_mail import Message

from sqlalchemy import func
from datetime import datetime



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully registered!')
        return redirect(url_for('login'))
    return render_template('registration.html', pagename="Registration Page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # form = userlogin()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # User authentication logic here (e.g., setting a session)
            session['userlogged'] = user.id
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', pagename='Login Page')

@app.route('/add_expense/', methods=['POST'])
def add_expense():
    if 'userlogged' in session:
        current_user_id = session['userlogged']
        category = request.form['category']
        amount = request.form.get('amount', type=float)  # Safely get amount as float
        expense_date = request.form['date']
        
        # Parse the date from the form input
        try:
            date_object = datetime.strptime(expense_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.')
            return redirect(url_for('dashboard'))

        # Create a new Expense object including the date
        new_expense = Expense(category=category, amount=amount, user_id=current_user_id, date=date_object)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!')
    else:
        flash('You are not logged in!')
    
    return redirect(url_for('dashboard'))


@app.route('/logout/')
def logout():
    user = None  # Initialize user as None

    if session.get('userlogged') is not None:
        user = session.get('userlogged')
        # Assuming you have a database model for users named MyUser
        user = User.query.get(user)

        session.pop('userlogged', None)
        flash('You have been logged out', category='success')

    return redirect(url_for('homepage'))


@app.route("/")
def homepage():
    id= session.get('userlogged')
    user=db.session.query(User).get(id)
    config_items = app.config
    return render_template("index.html", pagename="Home Page",user=user, config_items=config_items)


@app.route('/dashboard')
def dashboard():
    if 'userlogged' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    current_user_id = session['userlogged']
    user = User.query.get(current_user_id)

    # Fetch individual expenses for the current user
    expenses_query = Expense.query.filter_by(user_id=current_user_id).all()
    expenses = [{
        'id': expense.id,
        'category': expense.category,
        'amount': expense.amount,
        'date': expense.date.strftime('%Y-%m-%d') if expense.date else None
    } for expense in expenses_query]

    # Aggregate expenses by month and category
    monthly_expenses_query = db.session.query(
        extract('year', Expense.date).label('year'),
        extract('month', Expense.date).label('month'),
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(Expense.user_id == current_user_id
    ).group_by('year', 'month', Expense.category
    ).order_by('year', 'month').all()

    # Convert query results to a list of dictionaries for monthly expenses
    monthly_expenses = [{
        'year_month': f"{year}-{str(month).zfill(2)}",
        'category_total': f"{category}: ${total}"
    } for year, month, category, total in monthly_expenses_query]

    return render_template("dashboard.html", user=user, expenses=expenses, monthly_expenses=monthly_expenses)



@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    # Make sure a user is logged i
    if 'userlogged' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('login'))
    
    # Retrieve the expense by ID
    expense_to_delete = Expense.query.get(expense_id)
    
    # If the expense does not exist, abort with a 404 error
    if expense_to_delete is None:
        flash('Expense not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check that the logged-in user is the owner of the expense
    if expense_to_delete.user_id == session['userlogged']:
        # Delete the expense
        db.session.delete(expense_to_delete)
        db.session.commit()
        flash('Expense deleted successfully.', 'success')
    else:
        # If the user is not the owner, do not allow them to delete it
        flash('You do not have permission to delete this expense.', 'danger')
    
    # Redirect back to the dashboard
    return redirect(url_for('dashboard'))


@app.route('/monthly_report')
def monthly_report_view():
    current_user_id = session.get('userlogged')
    if not current_user_id:
        flash('Please log in to access the monthly report.', 'warning')
        return redirect(url_for('login'))

    monthly_expenses = db.session.query(
        extract('year', Expense.date).label('year'),
        extract('month', Expense.date).label('month'),
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user_id
    ).group_by('year', 'month', Expense.category
    ).order_by('year', 'month').all()

    # Convert query results into a nested structure if needed or keep as is
    # For simplicity, assuming direct pass-through here
    expenses_data = [{'month': month, 'category': category, 'total': total} for year, month, category, total in monthly_expenses]

    return render_template("monthly_report.html", monthly_expenses=expenses_data)


@app.route('/some_route')
def some_view_function():
    # Example data - replace with your actual logic to get `report`
    report = {
        'category1': 100,
        'category2': 150,
        'category3': 200,
    }

    # Ensure you're passing a dictionary if expecting to call .items() in the template
    return render_template("your_template.html", report=report)