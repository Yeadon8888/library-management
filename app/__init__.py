from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @app.template_filter('now')
    def now_filter(f):
        return datetime.utcnow()
        
    @app.template_filter('avg')
    def avg_filter(lst):
        return sum(lst) / len(lst) if lst else 0
    
    from app.routes import main, auth, book, loan
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(book.bp)
    app.register_blueprint(loan.bp)
    
    @login_manager.user_loader
    def load_user(id):
        from app.models.user import User
        return User.query.get(int(id))
    
    return app 