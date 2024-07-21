from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user, logout_user
from app import db
from app.models import Prompt, Category, Model, Rating
from app.forms import LoginForm, RegistrationForm, PromptForm, CategoryForm, ModelForm

bp = Blueprint('main', __name__)

# Rota principal
@bp.route('/')
@login_required
def index():
    return redirect(url_for('main.list_prompts'))

# Rota para listar prompts
@bp.route('/list_prompts', methods=['GET', 'POST'])
@login_required
def list_prompts():
    prompts = Prompt.query.all()
    models = Model.query.all()
    categories = Category.query.all()
    prompts_with_ratings = []

    for prompt in prompts:
        average_rating = db.session.query(db.func.avg(Rating.score)).filter(Rating.prompt_id == prompt.id).scalar()
        user_rating = Rating.query.filter_by(prompt_id=prompt.id, user_id=current_user.id).first()
        user_rating_score = user_rating.score if user_rating else 0
        prompts_with_ratings.append({
            'prompt': prompt,
            'average_rating': average_rating,
            'user_rating': user_rating_score
        })

    return render_template('list_prompts.html', title='Prompts', prompts_with_ratings=prompts_with_ratings, models=models, categories=categories)

# Rota para adicionar um novo prompt
@bp.route('/add_prompt', methods=['GET', 'POST'])
@login_required
def add_prompt():
    form = PromptForm()
    if form.validate_on_submit():
        prompt = Prompt(
            name=form.name.data,
            text=form.text.data,
            role=form.role.data,
            temperature=form.temperature.data,
            model_id=form.model.data,
            author_id=current_user.id,
        )
        db.session.add(prompt)
        db.session.commit()
        flash('Prompt adicionado com sucesso.', 'success')
        return redirect(url_for('main.list_prompts'))
    return render_template('add_prompt.html', title='Adicionar Novo Prompt', form=form)

# Rota para editar um prompt existente
@bp.route('/edit_prompt/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_prompt(id):
    prompt = Prompt.query.get_or_404(id)
    form = PromptForm(obj=prompt)
    if form.validate_on_submit():
        prompt.name = form.name.data
        prompt.text = form.text.data
        prompt.role = form.role.data
        prompt.temperature = form.temperature.data
        prompt.model_id = form.model.data
        db.session.commit()
        flash('Prompt atualizado com sucesso.', 'success')
        return redirect(url_for('main.list_prompts'))
    return render_template('edit_prompt.html', title='Editar Prompt', form=form)

# Rota para excluir prompts
@bp.route('/delete_prompts', methods=['POST'])
@login_required
def delete_prompts():
    data = request.get_json()
    ids_to_delete = data.get('ids', [])

    if ids_to_delete:
        for prompt_id in ids_to_delete:
            prompt = Prompt.query.get(prompt_id)
            if prompt:
                db.session.delete(prompt)
        db.session.commit()
        flash('Prompts excluídos com sucesso.', 'success')
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='Nenhum prompt selecionado.')

# Rota para listar categorias
@bp.route('/list_categories', methods=['GET', 'POST'])
@login_required
def list_categories():
    categories = Category.query.all()
    return render_template('list_categories.html', title='Categorias', categories=categories)

# Rota para adicionar uma nova categoria
@bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Categoria adicionada com sucesso.', 'success')
        return redirect(url_for('main.list_categories'))
    return render_template('add_category.html', title='Adicionar Nova Categoria', form=form)

# Rota para editar uma categoria existente
@bp.route('/edit_category/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Categoria atualizada com sucesso.', 'success')
        return redirect(url_for('main.list_categories'))
    return render_template('edit_category.html', title='Editar Categoria', form=form)

# Rota para excluir categorias
@bp.route('/delete_categories', methods=['POST'])
@login_required
def delete_categories():
    data = request.get_json()
    ids_to_delete = data.get('ids', [])

    if ids_to_delete:
        for category_id in ids_to_delete:
            category = Category.query.get(category_id)
            if category:
                db.session.delete(category)
        db.session.commit()
        flash('Categorias excluídas com sucesso.', 'success')
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='Nenhuma categoria selecionada.')

# Rota para listar modelos
@bp.route('/list_models', methods=['GET', 'POST'])
@login_required
def list_models():
    models = Model.query.all()
    return render_template('list_models.html', title='Modelos', models=models)

# Rota para adicionar um novo modelo
@bp.route('/add_model', methods=['GET', 'POST'])
@login_required
def add_model():
    form = ModelForm()
    if form.validate_on_submit():
        model = Model(name=form.name.data)
        db.session.add(model)
        db.session.commit()
        flash('Modelo adicionado com sucesso.', 'success')
        return redirect(url_for('main.list_models'))
    return render_template('add_model.html', title='Adicionar Novo Modelo', form=form)

# Rota para editar um modelo existente
@bp.route('/edit_model/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_model(id):
    model = Model.query.get_or_404(id)
    form = ModelForm(obj=model)
    if form.validate_on_submit():
        model.name = form.name.data
        db.session.commit()
        flash('Modelo atualizado com sucesso.', 'success')
        return redirect(url_for('main.list_models'))
    return render_template('edit_model.html', title='Editar Modelo', form=form)

# Rota para excluir modelos
@bp.route('/delete_models', methods=['POST'])
@login_required
def delete_models():
    data = request.get_json()
    ids_to_delete = data.get('ids', [])

    if ids_to_delete:
        for model_id in ids_to_delete:
            model = Model.query.get(model_id)
            if model:
                db.session.delete(model)
        db.session.commit()
        flash('Modelos excluídos com sucesso.', 'success')
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='Nenhum modelo selecionado.')

# Rota para avaliar um prompt
@bp.route('/rate_prompt/<int:prompt_id>', methods=['POST'])
@login_required
def rate_prompt(prompt_id):
    data = request.get_json()
    rating_value = data.get('rating')

    rating = Rating.query.filter_by(prompt_id=prompt_id, user_id=current_user.id).first()
    if rating:
        rating.score = rating_value
    else:
        rating = Rating(prompt_id=prompt_id, user_id=current_user.id, score=rating_value)
        db.session.add(rating)

    db.session.commit()

    average_rating = db.session.query(db.func.avg(Rating.score)).filter(Rating.prompt_id == prompt_id).scalar()

    return jsonify(success=True, user_rating=rating_value, average_rating=average_rating)

# Rota para logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
