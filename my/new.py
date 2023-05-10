import json

json_str = '{"x": 1, "y": 0}'
my_dict = json.loads(json_str)

print(my_dict)  # Output: {'x': 1, 'y': 0}
