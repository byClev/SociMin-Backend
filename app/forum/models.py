from app.extensions import db
from sqlalchemy import func

class Forum(db.Model):
    __tablename__ = 'forums'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Forum {self.title}>'
    
class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_id = db.Column(db.String(32), nullable=True)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    forum = db.relationship('Forum', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<ForumPost {self.id} in Forum {self.forum_id}>'
    
class ForumComment(db.Model):
    __tablename__ = 'forum_comments'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    post = db.relationship('ForumPost', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<ForumComment {self.id} on Post {self.post_id}>'