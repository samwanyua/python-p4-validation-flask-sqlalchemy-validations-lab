from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Author must have a non-empty name.")
        existing_author = Author.query.filter(db.func.lower(Author.name) == db.func.lower(name)).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("Another author with this name already exists.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        phone_number_digits = ''.join(filter(str.isdigit, phone_number))
        if len(phone_number_digits) != 10:
            raise ValueError("Phone number must contain exactly ten digits.")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validates_content(self,key,content):
        if len(content.strip()) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Summary must be a maximum of 250 characters.')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either Fiction or Non-Fiction.')
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Title must contain one of the following phrases: "Won\'t Believe", "Secret", "Top", "Guess"')
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
