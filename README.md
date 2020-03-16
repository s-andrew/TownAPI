# Запуск
```buildoutcfg
docke-compose up
```

SwaggerUI: http://0.0.0.0:5000

# ТЗ
Требуется создать python веб-сервис. В качестве основы необходимо использовать один из
веб-фреймворков: flask(предпочтительно), django, tornado
Сервис должен предоставлять возможность редактирования регионов и городов, которые
входят в регионы.
Регионы – древовидная структура (имеется поле parent_id, которые ссылается на id)
Города – плоская структура, в которой имеется ссылка на регион.
Сервис должен предоставлять методы:
- 1 авторизации (остальные методы должны быть доступны только авторизованным
пользователям)
- 2 управления справочником регионов: добавление/изменение/удаление
- 3 управление справочником городов: добавление/изменение/удаление
- 4 просмотр всех регионов в виде дерева
- 5 просмотр городов в виде списка. Входной параметр:
  - 1 region_id. Если он передан – возвращаются только города из этого региона или всех дочерних к нему регионов.

Выходные данные из сервиса должны быть в json-формате
Данные по городам, регионам и пользователям должны храниться в реляционой БД. Доступ
из сервиса к ним необходимо осуществлять через ORM.