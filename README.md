Глобальные правки по проекту:
# TODO нужна человеческая документация по всему
#  проекту - докстринги, например, причем оформленные в каком-то общем стиле. Давай писать в гугловском стиле 
#   https://google.github.io/styleguide/pyguide.html
#  pydocstyle, только укажи в конфиге convention=google

# TODO заполни тайпинги везде

# TODO есть смысл небольшого рефакторинга вьюх и сервисов. если функция уже в файле flat.py, незачем 
#  называть функцию create_flat, если она создает flat.
# НО - есть смысл уточнять, если это create_comment

# TODO если не знаешь, как разбить приложение на
   аппкиЮ пользуйся проектирование БД и старайся избегать 
   перекрещивания связей - в итоге образованные группы станут более очевидными

# TODO в API не нужно создавать сессии БД в сервисах, заведи fast_api.Depends и юзай в API
#   https://fastapi.tiangolo.com/tutorial/sql-databases/


# В целом Depends полезны. Напоминалка:
Depends 
-- Depends
-- Depends
----Header
----Header
----Depends
------Header
------Query

https://fastapi.tiangolo.com/tutorial/dependencies/
