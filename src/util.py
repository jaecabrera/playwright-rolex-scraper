from datetime import datetime
from typing import Union, Dict, Any, List, Type
import pandas as pd
import janitor


JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


def insert_datetime():
    return datetime.now().strftime('%d-%m-%Y')


class Pipe:

    def __init__(self, data: JSON):
        self.input = data

    def run(self):
        clean_data = pd.DataFrame(self.input['@graph'][1]['offers'])
        clean_data = clean_data\
            .drop(['@type', 'availability', 'image'], axis=1)\
            .assign(date=insert_datetime())\
            .reorder_columns(['date'])

        return clean_data
