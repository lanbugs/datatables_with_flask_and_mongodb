# datatable_helpers.py

import re
from bson.json_util import dumps
import json
from flask import request


def get_paginated_filtered_sorted_data(collection, columns, search_columns=None):
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))
    draw = int(request.args.get('draw', 1))
    search_value = request.args.get('search[value]', '')  # Search term

    order_column = int(request.args.get('order[0][column]', 0))  # Default column index
    order_dir = request.args.get('order[0][dir]', 'asc')  # Default direction

    column_map = {i: col for i, col in enumerate(columns)}
    sort_field = column_map.get(order_column, columns[0])  # Default to the first column
    sort_direction = 1 if order_dir == "asc" else -1  # Ascending or descending

    search_fields = search_columns if search_columns else columns

    query = {}
    if search_value:
        regex = re.compile(search_value, re.IGNORECASE)
        query = {
            "$or": [{col: regex} for col in search_fields]
        }

    data_cursor = collection.find(query).sort(sort_field, sort_direction).skip(start).limit(length)
    data = list(data_cursor)

    records_filtered = collection.count_documents(query)
    records_total = collection.count_documents({})

    return {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": json.loads(dumps(data))
    }


def get_filtered_and_sorted_data_for_export(collection, columns, search_columns=None):
    search_value = request.args.get('search[value]', '')  # Search term

    order_column = int(request.args.get('order[0][column]', 0))  # Default column index
    order_dir = request.args.get('order[0][dir]', 'asc')  # Default direction

    column_map = {i: col for i, col in enumerate(columns)}
    sort_field = column_map.get(order_column, columns[0])  # Default to the first column
    sort_direction = 1 if order_dir == "asc" else -1  # Ascending or descending

    search_fields = search_columns if search_columns else columns

    query = {}
    if search_value:
        regex = re.compile(search_value, re.IGNORECASE)
        query = {
            "$or": [{col: regex} for col in search_fields]
        }

    data_cursor = collection.find(query).sort(sort_field, sort_direction)
    data = list(data_cursor)

    records_filtered = collection.count_documents(query)
    records_total = collection.count_documents({})

    return {
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": json.loads(dumps(data))
    }


def generate_datatables_script(url_path, columns, table_id="dataTable"):
    columns_js = ",\n                ".join([f'{{ "data": "{col}" }}' for col in columns])

    script = f"""
    <script>
        $(document).ready(function() {{
            $('#{table_id}').DataTable({{
                "processing": true,
                "serverSide": true,
                "ajax": {{
                    "url": "{url_path}",
                    "type": "GET"
                }},
                "columns": [
                    {columns_js}
                ],
                "language": {{
                    "paginate": {{
                        "first": "First",
                        "last": "Last",
                        "next": "Next",
                        "previous": "Previous"
                    }},
                    "search": "Search:",
                    "processing": "Loading..."
                }},
                "order": [[0, "asc"]]
            }});
        }});
    </script>
    """
    return script
