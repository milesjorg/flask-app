from app.models import User

def get_user(user_id=None, username=None):
    if not user_id and not username:
        return
    if user_id and username:
        return
    if user_id:
        user = User.query.get(user_id)
    else:
        user = User.query.filter_by(username=username).first()
    print(user)
    return user