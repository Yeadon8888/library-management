from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.loan import Loan
from app.models.book import Book
from app import db
from datetime import datetime, timedelta

bp = Blueprint('loan', __name__)

@bp.route('/book/<int:book_id>/borrow')
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # 检查是否有库存
    if book.available_copies <= 0:
        flash('该书已无库存')
        return redirect(url_for('book.book_detail', id=book_id))
        
    # 检查用户借书数量限制
    active_loans = Loan.query.filter_by(
        user_id=current_user.id,
        status='borrowed'
    ).count()
    
    if active_loans >= 5:  # 假设最多允许借5本书
        flash('已达到最大借书数量限制')
        return redirect(url_for('book.book_detail', id=book_id))
    
    # 创建借书记录
    loan = Loan(
        user_id=current_user.id,
        book_id=book_id,
        due_date=datetime.utcnow() + timedelta(days=30)  # 借期30天
    )
    
    # 更新图书库存
    book.available_copies -= 1
    
    db.session.add(loan)
    db.session.commit()
    
    flash('借书成功！')
    return redirect(url_for('book.book_detail', id=book_id))

@bp.route('/book/<int:book_id>/return')
@login_required
def return_book(book_id):
    loan = Loan.query.filter_by(
        user_id=current_user.id,
        book_id=book_id,
        status='borrowed'
    ).first_or_404()
    
    loan.return_date = datetime.utcnow()
    loan.status = 'returned'
    
    # 更新图书库存
    book = Book.query.get(book_id)
    book.available_copies += 1
    
    db.session.commit()
    
    flash('还书成功！')
    return redirect(url_for('book.book_detail', id=book_id))

@bp.route('/my-loans')
@login_required
def my_loans():
    loans = Loan.query.filter_by(user_id=current_user.id).all()
    current_time = datetime.utcnow()  # 添加当前时间
    return render_template('loan/my_loans.html', loans=loans, current_time=current_time)

def check_overdue_loans():
    overdue_loans = Loan.query.filter(
        Loan.status == 'borrowed',
        Loan.due_date < datetime.utcnow()
    ).all()
    
    for loan in overdue_loans:
        loan.status = 'overdue'
        # 这里可以添加发送邮件提醒的功能
    
    db.session.commit() 