TEXT = "леопард не может изменить своих пятен."
ALPHABET = list("абвгдежзийклмнопрстуфхцчшщъыьэюя")
EXTRA_ALPHABET = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
ALPHABET_LENGTH = len(ALPHABET)
EXTRA_ALPHABET_LENGTH = ALPHABET_LENGTH + 1
SEPARATION_PERIOD = 5

def prepare_text(text: str):
    '''
    Пробелы не учитываются -> убираем их, точки и запятые заменяются на ТЧК и ЗПТ
    '''
    return text.lower().replace(' ', '').replace('.', 'тчк').replace(',', 'зпт')
