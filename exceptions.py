class ParseException(Exception):
    def __init__(self):
        self.args = ('Ошибка при обработки данных для таблицы курсв', )


class GetTableFromWebException(Exception):
    def __init__(self):
        self.args = ('Ошибка получения данных для составления таблицы курса', )
