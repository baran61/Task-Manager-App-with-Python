from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # A secret key is used for generating secure tokens and protecting your application
                                                  # against various security threats like cross-site
                                                  # request forgery (CSRF) attacks and session tampering.

print(app.config['SECRET_KEY'])  #Restarting with stat shows the secret key

# Define a list to store registered users (This is for demonstration purposes, not for production)
registered_users = []

tasks = [
        {'id': 1, 'title': 'Buy groceries', 'description': 'Pick up milk, bread, and eggs from the supermarket.'},
        {'id': 2, 'title': 'Complete project proposal',
         'description': 'Finish writing the project proposal for client X.'},
        {'id': 3, 'title': 'Schedule team meeting',
         'description': 'Set up a team meeting for next week to discuss project progress.'},
        {'id': 4, 'title': 'Prepare presentation',
         'description': 'Create slides for the upcoming conference presentation.'},
        {'id': 5, 'title': 'Call John', 'description': 'Call John to discuss the upcoming collaboration.'},
        {'id': 6, 'title': 'Review expenses', 'description': 'Go through the monthly expenses and categorize them.'},
        {'id': 7, 'title': 'Book flight tickets',
         'description': 'Book flight tickets for the business trip next month.'},
        {'id': 8, 'title': 'Update website content',
         'description': 'Add new blog posts and update product information on the website.'},
        {'id': 9, 'title': 'Send client invoice',
         'description': 'Email the invoice for the completed project to the client.'},
        {'id': 10, 'title': 'Organize team-building event',
         'description': 'Plan a team-building activity for the entire team.'},
        {'id': 11, 'title': 'Fix bug in application',
         'description': 'Investigate and fix the issue reported by the QA team.'},
        {'id': 12, 'title': 'Prepare quarterly report',
         'description': 'Compile data and create a report for the last quarter.'},
        {'id': 13, 'title': 'Attend webinar', 'description': 'Join the webinar on new marketing trends.'},
        {'id': 14, 'title': 'Recruit new team member',
         'description': 'Review applications and schedule interviews for the open position.'},
        {'id': 15, 'title': 'Create social media content',
         'description': 'Design and schedule social media posts for the next week.'},
        {'id': 16, 'title': 'Conduct product demo', 'description': 'Present the product demo to potential clients.'},
        {'id': 17, 'title': 'Setup new office space',
         'description': 'Coordinate with the facilities team to set up the new office.'},
        {'id': 18, 'title': 'Review marketing campaign',
         'description': 'Analyze the results of the latest marketing campaign.'},
        {'id': 19, 'title': 'Write user documentation',
         'description': 'Prepare user guides for the newly released feature.'},
        {'id': 20, 'title': 'Meet with project stakeholders',
         'description': 'Schedule a meeting with project stakeholders to discuss progress.'},
        {'id': 21, 'title': 'Review sales leads',
         'description': 'Follow up on potential sales leads and update the CRM system.'},
        {'id': 22, 'title': 'Prepare training materials',
         'description': 'Develop training materials for the upcoming employee training session.'},
        {'id': 23, 'title': 'Update inventory',
         'description': 'Update the inventory database with the latest stock information.'},
        {'id': 24, 'title': 'Create ad campaign',
         'description': 'Design and launch an ad campaign to increase brand awareness.'},
        {'id': 25, 'title': 'Coordinate project kickoff',
         'description': 'Arrange the project kickoff meeting with the client.'},
    ]

class TaskForm(FlaskForm):
        title = StringField('Task Title', validators=[DataRequired()])
        description = StringField('Description')
        submit = SubmitField('Add Task')

# Registration route and function
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Please fill in all the fields', 'error')
        elif any(user['username'] == username for user in registered_users):
            flash('Username already exists', 'error')
        else:
            registered_users.append({'username': username, 'password': password})
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Login route and function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in registered_users if user['username'] == username and user['password'] == password), None)
        if user:
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('index'))  # Redirect to the index page after successful login
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))  # If the login is not successful, redirect back to the login page

    # If the request is GET (not a login attempt), render the login.html template
    return render_template('login.html')


# Index route and function
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_task_id = len(tasks) + 1
        tasks.append({'id': new_task_id, 'title': title, 'description': description})
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', form=form, tasks=tasks)



@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
        task = next((t for t in tasks if t['id'] == task_id), None)
        if not task:
            flash('Task not found!', 'danger')
            return redirect(url_for('index'))

        form = TaskForm(obj=task)
        if form.validate_on_submit():
            task['title'] = form.title.data
            task['description'] = form.description.data
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('task_form.html', form=form, action='edit', task_id=task_id)


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
        task = next((t for t in tasks if t['id'] == task_id), None)
        if not task:
            flash('Task not found!', 'danger')
        else:
            task['completed'] = True
            flash('Task marked as completed!', 'success')
        return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
        global tasks
        tasks = [t for t in tasks if t['id'] != task_id]
        flash('Task deleted successfully!', 'success')
        return redirect(url_for('index'))







if __name__ == '__main__':
        app.run(debug=True)
