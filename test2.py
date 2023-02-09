import json

list = ['id', 'nam1', 'name2', '1x3', [['1', '2', '3'], ['1.2', '2.3', '4.5']], '122x',
        [['1', '2', '3'], ['1.2', '2.3', '4.5']]]


jsonString = json.dumps(list)
