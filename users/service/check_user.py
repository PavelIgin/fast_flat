from fastapi import status, HTTPException


async def check_user(user, id_owner):
    # TODO можно удалить. Но если где-то понадобится проверить доступ, как
    #  вариант, это можно сделать на уровне вьюхи, в Вepends.
    if id_owner != user.id:
        raise HTTPException(detail='Permission denied', status_code=status.HTTP_400_BAD_REQUEST)
