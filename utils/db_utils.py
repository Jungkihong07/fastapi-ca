from sqlalchemy import inspect

# 자동으로 할당되어 만들어주는 코드로 보인다.
def row_to_dict(row) -> dict:
    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}