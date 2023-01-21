from fastapi import status, HTTPException


async def check_user(user, id_owner):
    if id_owner != user.id:
        raise HTTPException(detail='Permission denied', status_code=status.HTTP_400_BAD_REQUEST)
