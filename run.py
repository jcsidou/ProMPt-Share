from app import create_app, db
from app.models import User, Prompt, Category, Model

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Prompt': Prompt, 'Category': Category, 'Model': Model}

if __name__ == "__main__":
    app.run(debug=True)
