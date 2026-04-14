# for name in dir(__builtins__):
#     obj = getattr(__builtins__, name)
#     if callable(obj):
#         doc = obj.__doc__
#         if doc:
#             print(name, "-", doc.split("\n")[0])
#         else:
#             print(name, "-", "No doc available")

# x = [
#     "teste", "teste"
# ]

# if type(x) == list:
#     print("É uma lista")

# for error in Exception.__subclasses__():
#     print(error.__name__)

teste1 = {
    "key1": "value1",
    "key2": "value2"
}

teste2 = {
    "key3": "value3",
    "key4": "value4"
}

lista =  [{'log_level': 'NOTICE', 'log_message': 'Connection to server'}, {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]

alvo = [d['log_level'] + ': ' + d['log_message'] for d in lista]

# str()

# for dictionary in lista:
#     for value in dictionary.values():
#         alvo.append(value)

print(alvo[0])