from core.frontend import templates
from core.users import current_user
from fastapi import Depends, Request
from models.user import User

# def role_is_manager_or_superuser(
#     user: User = Depends(current_user)
# ) -> bool:
#     print(user)
#     if user and (user.is_manager or user.is_superuser):
#         return True
#     return False

# templates.env.filters['manager_or_superuser'] = role_is_manager_or_superuser
