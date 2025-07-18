from bot.utils.keyboard_utils import *
from bot.utils.message_utils import *


def insert_test():
    INSERT_TEXT_TESTS = (
        {'text': 'gjkladjhjg ? fjhsd? dshfahsdl? ? hladf?',
         'new': (1, 3, 4, 5, 4),
         'truth': 'gjkladjhjg 1 fjhsd3 dshfahsdl4 5 hladf4'},
        {'text': 'jhfjhads: ?, ?, ?. done, ?.',
         'new': ('apple', 'orange', 'cake', 'pasta'),
         'truth': 'jhfjhads: apple, orange, cake. done, pasta.'}
    )

    for test in INSERT_TEXT_TESTS:
        answer = insert_text(test['text'], test['new'])
        if answer == test['truth']:
            print('done')
        else:
            print(answer, test['truth'])


def test_list_message():
    TESTS = (
        {'l': ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'z', 'c', 'x', 'y'),
         'c': 5},
        {'l': ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'z', 'c', 'x', 'y'),
         'c': 2},
        {'l': ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'z', 'c', 'x'),
         'c': 1}
    )

    for test in TESTS:
        lists, column = test.get('l'), test.get('c')
        print(column)
        print(create_list_message(lists, column))


if __name__ == '__main__':
    test_list_message()