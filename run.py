from app import create_app, db
from app.models.user import User
from app.models.book import Book
from app.models.loan import Loan
from app.models.comment import Comment
from app.models.reservation import Reservation

app = create_app()

# 创建数据库上下文
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Book': Book,
        'Loan': Loan,
        'Comment': Comment,
        'Reservation': Reservation
    }

if __name__ == '__main__':
    # 确保数据库表存在
    with app.app_context():
        db.create_all()
        
        # 创建管理员账户（如果不存在）
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')  # 在生产环境中请使用更强的密码
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True) 
    