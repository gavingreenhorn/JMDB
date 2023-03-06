import csv
import os
from typing import AnyStr, Dict, List


def get_csv_data(source) -> List[Dict]:
    """Load test data from csv as python dict."""
    path = f'static/data/{source}.csv'
    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            path
        ), 'r'
    ) as file:
        csv_dict = csv.DictReader(file)
        return [{attr: row.get(attr) for attr in row} for row in csv_dict]


def set_by_id(payload: Dict, field: AnyStr) -> None:
    """Rename incoming dict key to the foreign key name."""
    payload[f'{field}_id'] = payload.pop(field)
