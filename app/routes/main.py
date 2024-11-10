from flask import Blueprint, render_template
from app.models.book import Book

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # 获取最新添加的图书
    recent_books = Book.query.order_by(Book.id.desc()).limit(6).all()
    return render_template('main/index.html', recent_books=recent_books) 