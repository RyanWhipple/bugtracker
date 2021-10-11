from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.bug import Bug
from flask_app.models.update import Update
from flask_app.models.user import User

# All Bugs Dashboard
@app.route('/bugs')
def bugs():
    if not 'user_id' in session:
            return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    bugs = Bug.get_all_bugs_with_last_update()

    return render_template(
        'bugs.html',
        user = user,
        bugs = bugs,
        )


# Save a Bug
@app.route('/bugs/new', methods=['POST'])
def bug_save():
    if not 'user_id' in session:
        return redirect('/')
    
    if not Bug.validate_bug(request.form):
        return redirect('/bugs')

    data = {
        'title'         : request.form['title'],
        'description'   : request.form['description'],
        'user_id'       : session['user_id'],
        'status'        : "Open",
    }

    Bug.add_bug(data)
    return redirect("/bugs")


# View a Bug
@app.route('/bug/<int:bug_id>', methods=['GET', 'POST'])
def bug_view(bug_id):
    if not 'user_id' in session:
        return redirect('/')
    else:
        # Users
        data = {
            'id': session['user_id']
        }
        user = User.get_by_id(data)
        
        # Bugs
        data = {
            'id'    : bug_id
        }
        bug = Bug.get_bug_by_id_with_user_data(data)

        # Updates
        data = {
            'id'    : bug_id
        }
        updates = Update.get_updates_by_bug_id_with_user_data(data)

        # Developers
        data = {
            'id'    : bug_id
        }
        developers = Bug.get_bug_by_id_with_developer_names(data)

        if len(updates) > 0:
            last_update = updates[0]
        else:
            last_update = None

        print("Developers:", developers)

        return render_template(
            'bug.html',
            user            = user,
            bug             = bug,
            updates         = updates,
            last_update     = last_update,
            developers      = developers,
        )

# update a Bug
@app.route('/bug/update/<int:bug_id>', methods=['GET', 'POST'])
def bug_update(bug_id):
    if not 'user_id' in session:
        return redirect('/')
    
    if not Update.validate_update(request.form):
        return redirect(f'/bug/{bug_id}')

    if request.form.get('closeBug'):
        print("Bug is closed!")
        data = {
            'id'    : bug_id
        }
        Bug.close(data)

    data = {
        'bug_id'        : bug_id,
        'description'   : request.form['description'],
        'user_id'       : session['user_id'],
    }

    Update.add_update(data)
    return redirect(f"/bug/{bug_id}")