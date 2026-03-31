import math


def calculator(operation: str, a: float, b: float) -> str:
    """Perform a basic arithmetic operation on two numbers.

    Args:
        operation: The math operation to perform. Must be one of: "add", "subtract", "multiply", "divide", "power", "modulo", "sqrt", "round".
        a: The first number. For sqrt and round, this is the only number used.
        b: The second number. For sqrt and round, pass 0 (it will be ignored).

    Returns:
        The result of the operation as a string.
    """
    match operation:
        case "add":
            result = a + b
        case "subtract":
            result = a - b
        case "multiply":
            result = a * b
        case "divide":
            if b == 0:
                return "Error: Division by zero."
            result = a / b
        case "power":
            result = a ** b
        case "modulo":
            if b == 0:
                return "Error: Division by zero."
            result = a % b
        case "sqrt":
            if a < 0:
                return "Error: Cannot take square root of a negative number."
            result = math.sqrt(a)
        case "round":
            result = round(a)
        case _:
            return f"Error: Unknown operation '{operation}'. Use add, subtract, multiply, divide, power, modulo, sqrt, or round."
    return str(result)
