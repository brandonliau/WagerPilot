def div(x: float, y: float) -> float:
    try:
        return x/y
    except (TypeError, ZeroDivisionError):
        return 0
