from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.thought import Thought
from flask_app.models.user import User


# Dashboard View
@app.route('/thoughts')
def thoughts_dashboard():
    if not 'user_id' in session:
            return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_one_user_with_thoughts(data)
    thoughts = Thought.get_all_thoughts()
    thoughts_user_liked = Thought.get_all_users_liked_thoughts(data)

    return render_template  ('thoughts.html', user = user, thoughts=thoughts, thoughts_user_liked = thoughts_user_liked)


# "Like" a Thought
@app.route('/thoughts/<int:thought_id>/like')
def like(thought_id):
    data = {
        "thought_id"    :   thought_id,
        "user_id"       :   session['user_id']
    }
    Thought.like_thought(data)
    return redirect('/thoughts')


# "Dislike" a Thought
@app.route('/thoughts/<int:thought_id>/dislike')
def dislike(thought_id):
    data = {
        "thought_id"    :   thought_id,
        "user_id"       :   session['user_id']
    }
    Thought.dislike_thought(data)
    return redirect('/thoughts')


# Save a Thought
@app.route('/users/<int:user_id>/thought', methods=['GET', 'POST'])
def thoughts_save(user_id):
    if not 'user_id' in session:
        return redirect('/')
    
    if not Thought.validate_thought(request.form):
        return redirect('/thoughts')

    data = {
        'content': request.form['content'],
        'user_id': session['user_id'],
    }

    Thought.add_thought(data)
    return redirect("/thoughts")


# Delete a Thought
@app.route('/thoughts/<int:id>/delete', methods=['GET', 'POST'])
def delete_thought(id):
    data = {
        'id': id,
    }
    Thought.delete(data)
    return redirect('/thoughts')