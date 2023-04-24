# flaskr/recipe.py

# 1. Import necessary modules and create a blueprint.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('recipe', __name__)

# 2. Define the index view function.
@bp.route('/')
def index():
    db = get_db()
    recipes = db.execute(
        'SELECT r.id, title, description, instructions, created, author_id, username'
        ' FROM recipe r JOIN user u ON r.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('recipe/index.html', recipes=recipes)

# 3. Define the create view function.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        instructions = request.form['instructions']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO recipe (title, description, instructions, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, description, instructions, g.user['id'])
            )
            db.commit()
            return redirect(url_for('recipe.index'))

    return render_template('recipe/create.html')

# 4. Define the update view function.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    recipe = get_recipe(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        instructions = request.form['instructions']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE recipe SET title = ?, description = ?, instructions = ?'
                ' WHERE id = ?',
                (title, description, instructions, id)
            )
            db.commit()
            return redirect(url_for('recipe.index'))

    return render_template('recipe/update.html', recipe=recipe)

# 5. Define the delete view function.
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_recipe(id)
    db = get_db()
    db.execute('DELETE FROM recipe WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('recipe.index'))

# 6. Create a helper function, get_recipe(), to avoid code duplication.
def get_recipe(id, check_author=True):
    recipe = get_db().execute(
        'SELECT r.id, title, description, instructions, created, author_id, username'
        ' FROM recipe r JOIN user u ON r.author_id = u.id'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

    if recipe is None:
        abort(404, f"Recipe id {id} doesn't exist.")

    if check_author and recipe['author_id'] != g.user['id']:
        abort(403)

    return recipe

# 7. Define the search view function.
@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        db = get_db()
        recipes = db.execute(
            "SELECT r.id, title, description, instructions, created, author_id, username"
            " FROM recipe r JOIN user u ON r.author_id = u.id"
            " WHERE title LIKE ?"
            " ORDER BY created DESC",
            (f"%{search_query}%",)
        ).fetchall()
        return render_template('recipe/search.html', recipes=recipes, search_query=search_query)

    return render_template('recipe/search.html')
