from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    return {'year': datetime.now().year}

# def year(request):
#     """Добавляет переменную с текущим годом."""
#     current_year = datetime.now().year
#     return {'year': current_year}
