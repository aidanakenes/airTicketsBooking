class PassengersNumberError(Exception):
    msg: str = 'Количество пассажиров должно быть больше 0'
    status_code: int = 404


class SearchNotFound(Exception):
    msg: str = 'Нет данных по результатам поиска'
    status_code: int = 404


class BookNotFound(Exception):
    msg: str = 'Нет данных по результатам поиска брони'
    status_code: int = 404


class InvalidParams(Exception):
    msg: str = 'Неправльно указаны параметры'
    status_code: int = 404
