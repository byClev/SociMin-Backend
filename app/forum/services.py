from app.forum.models import Forum, ForumPost, ForumComment
from app.extensions import db

class ForumService:
    
    def create_forum(self, title: str, description: str, user_id: int) -> Forum:
        forum = Forum(title=title, description=description, user_id=user_id)
        db.session.add(forum)
        db.session.commit()
        return forum
    
    def get_forums(self, user_id: int = None, page: int = 1, per_page: int = 10):
        if user_id is not None:
            return Forum.query.filter_by(user_id=user_id).order_by(Forum.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return Forum.query.order_by(Forum.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_forum_by_id(self, forum_id: int) -> Forum:
        return Forum.query.get(forum_id)
    
    def update_forum(self, forum_id: int, title: str = None, description: str = None) -> Forum:
        forum = Forum.query.get(forum_id)
        if not forum:
            return None
        
        if title:
            forum.title = title
        if description:
            forum.description = description
        
        db.session.commit()
        return forum
    
    def delete_forum(self, forum_id: int, user_id: int) -> bool:
        forum = Forum.query.get(forum_id)
        if not forum:
            return False

        if forum.user_id != user_id:
            return False

        db.session.delete(forum)
        db.session.commit()
        return True
# Post services------------------------------------------------------------------------------------------
    def create_post(self, forum_id: int, user_id: int, title: str, content: str, image_id: str = None, video_url: str = None) -> ForumPost:
        post = ForumPost(forum_id=forum_id, user_id=user_id, title=title, content=content, image_id=image_id, video_url=video_url)
        db.session.add(post)
        db.session.commit()
        return post
    
    def get_post_by_id(self, post_id: int) -> ForumPost:
        return ForumPost.query.get(post_id)
    
    def get_posts_filtered(self, forum_id: int, user_id: int = None, page: int = 1, per_page: int = 10):
        query = ForumPost.query
        if forum_id is not None:
            query = query.filter_by(forum_id=forum_id)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        return query.order_by(ForumPost.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    def update_post(self, post_id: int, user_id: int, title: str = None, content: str = None, image_id: str = None, video_url: str = None) -> ForumPost:
        post = ForumPost.query.get(post_id)
        if not post:
            return None
        if post.user_id != user_id:
            return None

        if title:
            post.title = title
        if content:
            post.content = content
        if video_url is not None:  # String vazia é diferente de None, permite remover o vídeo
            post.video_url = video_url
        if image_id is not None:  # Sting vazia é diferente de None, permite remover a imagem
            post.image_id = image_id
        
        db.session.commit()
        return post
    
    def delete_post(self, post_id: int, user_id: int) -> bool:
        post = ForumPost.query.get(post_id)
        if not post:
            return False
        if post.user_id != user_id:
            return False

        db.session.delete(post)
        db.session.commit()
        return True

# Comment services------------------------------------------------------------------------------------------
    def create_comment(self, post_id: int, user_id: int, content: str) -> ForumComment:
        comment = ForumComment(post_id=post_id, user_id=user_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return comment

    def get_comment_by_id(self, comment_id: int) -> ForumComment:
        return ForumComment.query.get(comment_id)

    def get_comments_filtered(self, post_id: int = None, user_id: int = None, page: int = 1, per_page: int = 10):
        query = ForumComment.query
        if post_id is not None:
            query = query.filter_by(post_id=post_id)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        return query.order_by(ForumComment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    def update_comment(self, comment_id: int, user_id: int, content: str) -> ForumComment:
        comment = ForumComment.query.get(comment_id)
        if not comment:
            return None
        if comment.user_id != user_id:
            return None

        comment.content = content
        db.session.commit()
        return comment

    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        comment = ForumComment.query.get(comment_id)
        if not comment:
            return False
        if comment.user_id != user_id:
            return False

        db.session.delete(comment)
        db.session.commit()
        return True
    
forum_service = ForumService()