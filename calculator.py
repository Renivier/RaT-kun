def Tokenize(equation):
    tokens = []
    current = ''
    i = 0
    while i < len(equation):
        c = equation[i]

        if c.isdigit() or c == '.':
            current += c

        elif c == '-' and (i == 0 or equation[i - 1] in '(*+-/'):
            current = '-'

        else:
            if current:
                tokens.append(float(current))
                current = ''
            tokens.append(c)
        i += 1

    if current:
        tokens.append(float(current))

    implicit_fixed = []
    for j in range(len(tokens)):
        implicit_fixed.append(tokens[j])
        if j < len(tokens) - 1:
            a, b = tokens[j], tokens[j + 1]
            if (isinstance(a, (int, float)) or a == ')') and b == '(':
                implicit_fixed.append('*')
            elif a == ')' and isinstance(b, (int, float)):
                implicit_fixed.append('*')

    return implicit_fixed


def recursive_parser(tokens):
    parsed = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '(':
            sublist, total_consumed = recursive_parser(tokens[i + 1:])
            parsed.append(sublist)
            i += total_consumed + 1
        elif tokens[i] == ')':
            return parsed, i
        else:
            parsed.append(tokens[i])
        i += 1
    return parsed, i


# --- Evaluation ---
def eval_mul_div(tokens):
    i = 0
    while i < len(tokens):
        if isinstance(tokens[i], list):
            tokens[i] = evaluate(tokens[i])
        elif tokens[i] == '*':
            tokens[i - 1:i + 2] = [float(tokens[i - 1]) * float(tokens[i + 1])]
            i -= 1
        elif tokens[i] == '/':
            tokens[i - 1:i + 2] = [float(tokens[i - 1]) / float(tokens[i + 1])]
            i -= 1
        else:
            i += 1
    return tokens


def eval_add_sub(tokens):
    i = 0
    while i < len(tokens):
        if isinstance(tokens[i], list):
            tokens[i] = evaluate(tokens[i])
        elif tokens[i] == '+':
            tokens[i - 1:i + 2] = [float(tokens[i - 1]) + float(tokens[i + 1])]
            i -= 1
        elif tokens[i] == '-':
            tokens[i - 1:i + 2] = [float(tokens[i - 1]) - float(tokens[i + 1])]
            i -= 1
        else:
            i += 1
    return tokens


def evaluate(tokens):
    tokens = [evaluate(t) if isinstance(t, list) else t for t in tokens]

    tokens = eval_mul_div(tokens)
    tokens = eval_add_sub(tokens)

    if len(tokens) != 1:
        raise ValueError(f"Evaluation did not reduce to a single number: {tokens}")
    return tokens[0]


def calculate_expression(expr: str):
    expr = expr.replace(' ', '')
    tokens = Tokenize(expr)
    parsed = recursive_parser(tokens)[0]
    return evaluate(parsed)


if __name__ == "__main__":
    expr = input("What's your equation: ")
    try:
        result = calculate_expression(expr)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
