from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.book import Book
from app.models.comment import Comment
from app import db
from sqlalchemy import or_

bp = Blueprint('book', __name__)

@bp.route('/books')
def book_list():
    books = Book.query.all()
    return render_template('book/list.html', books=books)

@bp.route('/book/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('book/detail.html', book=book)

@bp.route('/book/add', methods=['GET', 'POST'])
@login_required
def book_add():
    if not current_user.is_admin:
        flash('权限不足')
        return redirect(url_for('book.book_list'))
        
    if request.method == 'POST':
        isbn = request.form['isbn']
        if Book.query.filter_by(isbn=isbn).first():
            flash('该ISBN号已存在')
            return redirect(url_for('book.book_add'))
            
        book = Book(
            isbn=isbn,
            title=request.form['title'],
            author=request.form['author'],
            publisher=request.form['publisher'],
            category=request.form['category'],
            total_copies=int(request.form['total_copies']),
            available_copies=int(request.form['total_copies'])
        )
        db.session.add(book)
        db.session.commit()
        flash('图书添加成功！')
        return redirect(url_for('book.book_list'))
        
    return render_template('book/add.html')

@bp.route('/books/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    books = Book.query
    if query:
        books = books.filter(or_(
            Book.title.ilike(f'%{query}%'),
            Book.author.ilike(f'%{query}%'),
            Book.isbn.ilike(f'%{query}%')
        ))
    if category:
        books = books.filter_by(category=category)
        
    books = books.all()
    return render_template('book/list.html', books=books)

@bp.route('/book/<int:book_id>/comment', methods=['POST'])
@login_required
def add_comment(book_id):
    book = Book.query.get_or_404(book_id)
    rating = int(request.form.get('rating', 0))
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('评论内容不能为空')
        return redirect(url_for('book.book_detail', id=book_id))
        
    if not 1 <= rating <= 5:
        flash('评分必须在1-5之间')
        return redirect(url_for('book.book_detail', id=book_id))
    
    # 检查用户是否已经评论过这本书
    existing_comment = Comment.query.filter_by(
        user_id=current_user.id,
        book_id=book_id
    ).first()
    
    if existing_comment:
        flash('您已经评论过这本书了')
        return redirect(url_for('book.book_detail', id=book_id))
    
    comment = Comment(
        user_id=current_user.id,
        book_id=book_id,
        content=content,
        rating=rating,
        is_approved=not current_user.is_admin  # 管理员评论自动通过
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('评论提交成功，等待管理员审核' if not current_user.is_admin else '评论发布成功')
    return redirect(url_for('book.book_detail', id=book_id))

@bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    if not current_user.is_admin:
        flash('权限不足')
        return redirect(url_for('main.index'))
        
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    
    flash('评论已通过审核')
    return redirect(url_for('book.book_detail', id=comment.book_id))

@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    # 只有评论作者和管理员可以删除评论
    if not (current_user.is_admin or current_user.id == comment.user_id):
        flash('权限不足')
        return redirect(url_for('book.book_detail', id=comment.book_id))
    
    db.session.delete(comment)
    db.session.commit()
    
    flash('评论已删除')
    return redirect(url_for('book.book_detail', id=comment.book_id))

@bp.route('/book/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def book_edit(id):
    if not current_user.is_admin:
        flash('权限不足')
        return redirect(url_for('book.book_list'))
        
    book = Book.query.get_or_404(id)
    
    if request.method == 'POST':
        book.isbn = request.form['isbn']
        book.title = request.form['title']
        book.author = request.form['author']
        book.publisher = request.form['publisher']
        book.category = request.form['category']
        new_total = int(request.form['total_copies'])
        
        # 计算新的可用库存
        borrowed = book.total_copies - book.available_copies
        book.total_copies = new_total
        book.available_copies = max(0, new_total - borrowed)
        
        try:
            db.session.commit()
            flash('图书信息更新成功！')
            return redirect(url_for('book.book_detail', id=id))
        except Exception as e:
            db.session.rollback()
            flash('更新失败：' + str(e))
            
    return render_template('book/edit.html', book=book)

@bp.route('/book/<int:id>/delete', methods=['POST'])
@login_required
def book_delete(id):
    if not current_user.is_admin:
        flash('权限不足')
        return redirect(url_for('book.book_list'))
        
    book = Book.query.get_or_404(id)
    
    # 检查是否有未归还的借阅
    active_loans = Loan.query.filter_by(
        book_id=id, 
        status='borrowed'
    ).count()
    
    if active_loans > 0:
        flash('该图书还有未归还的借阅记录，无法删除')
        return redirect(url_for('book.book_detail', id=id))
    
    try:
        db.session.delete(book)
        db.session.commit()
        flash('图书删除成功！')
        return redirect(url_for('book.book_list'))
    except Exception as e:
        db.session.rollback()
        flash('删除失败：' + str(e))
        return redirect(url_for('book.book_detail', id=id))