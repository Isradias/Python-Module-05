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

for error in Exception.__subclasses__():
    print(error.__name__)