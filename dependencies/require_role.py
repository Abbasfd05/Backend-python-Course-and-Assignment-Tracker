from fastapi import Depends, HTTPException, status
from models.user import UserModel
from models.role import UserRole
from dependencies.get_current_user import get_current_user


def require_role(*allowed_roles: UserRole):
    # docstring: A way of documenting something, or explain how it works.

    """
    Usage: Depends(require_role(UserRole.INSTRUCTOR))
    Raises 403 if the authenticated user's role isn't one of allowed_roles.
    """
    def dependency(current_user: UserModel = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action",
            )
        return current_user

    return dependency
