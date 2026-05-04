import ast
import re

def extract_param_types(code):
    tree = ast.parse(code)
    param_types = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        param_types.append(arg.annotation.id)
                    elif isinstance(arg.annotation, ast.Constant):
                        param_types.append(arg.annotation.s)
    return param_types

def extract_return_type(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.returns:
                if isinstance(node.returns, ast.Name):
                    return node.returns.id
                elif isinstance(node.returns, ast.Constant):
                    return node.returns.s
    return 'Any'

def extract_decorators(code):
    tree = ast.parse(code)
    decorators = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            decorators.extend([d.id for d in node.decorator_list if isinstance(d, ast.Name)])
    return decorators

def extract_imports(code):
    tree = ast.parse(code)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    return imports

# def extract_function_name(code):
#     tree = ast.parse(code)
#     for node in ast.walk(tree):
#         if isinstance(node, ast.FunctionDef):
#             return node.name
#     return None

def extract_function_name(content):
    # Pattern matches 'def' followed by whitespace and captures the function name
    pattern = r'def\s+([a-zA-Z_]\w*)'
    matches = re.search(pattern, content)
    if matches:
        return matches.group(1)
    return None