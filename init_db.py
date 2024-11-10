from app import create_app, db
from app.models.book import Book
from datetime import datetime

def init_books():
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 清空现有图书数据（可选）
        # Book.query.delete()
        
        # 准备示例图书数据
        books = [
            {
                'isbn': '9787536692930',
                'title': '三体',
                'author': '刘慈欣',
                'publisher': '重庆出版社',
                'category': '科技',
                'total_copies': 5,
                'available_copies': 5,
                'publish_date': datetime(2008, 1, 1)
            },
            {
                'isbn': '9787544253994',
                'title': '百年孤独',
                'author': '加西亚·马尔克斯',
                'publisher': '南海出版公司',
                'category': '文学',
                'total_copies': 3,
                'available_copies': 3,
                'publish_date': datetime(2011, 6, 1)
            },
            {
                'isbn': '9787508647357',
                'title': '人类简史',
                'author': '尤瓦尔·赫拉利',
                'publisher': '中信出版社',
                'category': '历史',
                'total_copies': 4,
                'available_copies': 4,
                'publish_date': datetime(2014, 11, 1)
            },
            {
                'isbn': '9787807463726',
                'title': '艺术的故事',
                'author': '贡布里希',
                'publisher': '广西美术出版社',
                'category': '艺术',
                'total_copies': 2,
                'available_copies': 2,
                'publish_date': datetime(2008, 4, 1)
            },
            {
                'isbn': '9787107242731',
                'title': '教育学原理',
                'author': '王道俊',
                'publisher': '人民教育出版社',
                'category': '教育',
                'total_copies': 6,
                'available_copies': 6,
                'publish_date': datetime(2009, 8, 1)
            },
            {
                'isbn': '9787020002207',
                'title': '红楼梦',
                'author': '曹雪芹',
                'publisher': '人民文学出版社',
                'category': '文学',
                'total_copies': 4,
                'available_copies': 4,
                'publish_date': datetime(1996, 1, 1)
            },
            {
                'isbn': '9787115546081',
                'title': 'Python编程：从入门到实践',
                'author': 'Eric Matthes',
                'publisher': '人民邮电出版社',
                'category': '科技',
                'total_copies': 3,
                'available_copies': 3,
                'publish_date': datetime(2020, 1, 1)
            }
        ]
        
        # 添加图书到数据库
        for book_data in books:
            # 检查ISBN是否已存在
            existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
            if not existing_book:
                book = Book(**book_data)
                db.session.add(book)
        
        try:
            db.session.commit()
            print("成功添加示例图书！")
        except Exception as e:
            db.session.rollback()
            print(f"添加图书时出错：{str(e)}")

if __name__ == '__main__':
    init_books() 