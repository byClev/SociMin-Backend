from app.extensions import db
from app.blog.models import BlogPost

class BlogService:

    def create_post(self, title: str, content: str, author_id: int, image_id: str = None, video_url: str = None) -> BlogPost:
        post = BlogPost(title=title, content=content, author_id=author_id, image_id=image_id, video_url=video_url)
        db.session.add(post)
        db.session.commit()
        return post
    
    def get_post_by_id(self, post_id: int) -> BlogPost:
        return BlogPost.query.get(post_id)
    
    def get_all_posts(self):
        return BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    
    def get_posts_by_author(self, author_id: int):
        return BlogPost.query.filter_by(author_id=author_id).order_by(BlogPost.created_at.desc()).all()
    
    def update_post(self, post_id: int, title: str = None, content: str = None, image_id: str = None, video_url: str = None) -> BlogPost:
        post = self.get_post_by_id(post_id)
        if not post:
            return None
        
        if title:
            post.title = title
        if content:
            post.content = content
        if image_id is not None:
            post.image_id = image_id
        if video_url is not None:
            post.video_url = video_url
        
        db.session.commit()
        return post
    
    def delete_post(self, post_id: int, author_id: int) -> bool:
        post = self.get_post_by_id(post_id)
        if not post:
            return False

        if post.author_id != author_id:
            return False

        db.session.delete(post)
        db.session.commit()
        return True
    
blog_service = BlogService()