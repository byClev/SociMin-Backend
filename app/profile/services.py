from app.profile.models import Profile, Contact
from app.extensions import db

class ProfileService:

    def create_profile(self, user_id: int, nickname: str, bio: str = None, avatar_id: str = None) -> Profile:
        if Profile.query.filter_by(user_id=user_id).first():
            raise ValueError("Profile already exists for this user.")
        
        profile = Profile(user_id=user_id, nickname=nickname, bio=bio, avatar_id=avatar_id)
        db.session.add(profile)
        db.session.commit()
        return profile

    def get_profile_by_user_id(self, user_id: int) -> Profile:
        return Profile.query.filter_by(user_id=user_id).first()

    def search_profiles(self, query: str, limit: int = 10) -> list[Profile]:
        return (
            Profile.query
            .filter(Profile.nickname.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )
    
    def update_profile(self, user_id: int, nickname: str = None, bio: str = None, avatar_id: str = None) -> Profile:
        profile = self.get_profile_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found.")
        
        if nickname is not None:
            profile.nickname = nickname
        if bio is not None:
            profile.bio = bio
        if avatar_id is not None:
            profile.avatar_id = avatar_id
        
        db.session.commit()
        return profile
    
    def delete_profile(self, user_id: int, profile_id: int) -> None:
        if user_id != profile_id:
            raise ValueError("You can only delete your own profile.")
        profile = self.get_profile_by_user_id(profile_id)
        if not profile:
            raise ValueError("Profile not found.")
        db.session.delete(profile)
        db.session.commit()

    def add_contact(self,user_id: int, profile_id: int, contact_profile_id: int) -> Contact:
        
        if user_id != profile_id:
            raise ValueError("You can only add contacts to your own profile.")

        if profile_id == contact_profile_id:
            raise ValueError("Cannot add yourself as a contact.")
        
        existing_contact = Contact.query.filter_by(profile_id=profile_id, contact_profile_id=contact_profile_id).first()
        if existing_contact:
            raise ValueError("Contact already exists.")
        
        contact = Contact(profile_id=profile_id, contact_profile_id=contact_profile_id)
        db.session.add(contact)
        db.session.commit()
        return contact
    
    def get_contacts(self, profile_id: int) -> list[Profile]:
        profile = Profile.query.get(profile_id)
        return [contact.contact_profile for contact in profile.contacts]
    
    def remove_contact(self, user_id: int, profile_id: int, contact_profile_id: int) -> None:

        if user_id != profile_id:
            raise ValueError("You can only remove contacts from your own profile.")
        
        contact = Contact.query.filter_by(profile_id=profile_id, contact_profile_id=contact_profile_id).first()
        if not contact:
            raise ValueError("Contact does not exist.")
        
        db.session.delete(contact)
        db.session.commit()

profile_service = ProfileService()