import importlib

# import inspect
from pathlib import Path

# from docstring_parser import parse

package_path = Path(__file__).parent
module_files = [
    file.stem for file in package_path.glob("*.py") if file.name != "__init__.py"
]


# def get_functions(user_functions: list = []):
#     for module_name in module_files:
#         module = importlib.import_module(f".{module_name}", __package__)
#         module = inspect.getmembers(module, inspect.isfunction)
#         for function_name, function_object in module:
#             original_function = (
#                 getattr(function_object, "__wrapped__", None) or function_object
#             )
#             user_functions.append(original_function)
#     return user_functions


# user_functions = get_functions()


# def get_commands(user_functions, user_commands=None):
#     if user_commands is None:
#         user_commands = []
#     for function in user_functions:
#         user_params = {}
#         parsed_docstring = parse(function.__doc__)
#         for param in parsed_docstring.params:
#             user_params[param.args[1]] = param.description
#         if user_params:
#             user_commands.append(user_params)
#     return user_commands


# user_commands = get_commands(user_functions)

user_labelers = [
    importlib.import_module(f".{module}", __package__).labeler
    for module in module_files
]
