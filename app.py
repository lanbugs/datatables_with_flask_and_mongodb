from flask import Flask, render_template, send_file, request
import re
from pymongo import MongoClient
import pandas as pd
from io import BytesIO
from datatable_helpers import get_paginated_filtered_sorted_data, generate_datatables_script, get_filtered_and_sorted_data_for_export

app = Flask(__name__)

client = MongoClient('mongodb://root:example@localhost:27017/')
db = client['testdb']

@app.route('/')
def mac_db_table():
    columns = ["mac", "name", "switch", "port"]
    table_id = "macTable"
    script = generate_datatables_script("/data/mac_db", columns, table_id=table_id)
    return render_template("index.html", table_title="MAC Database Table", columns=columns, table_id=table_id, script=script)


@app.route('/data/mac_db', methods=['GET'])
def load_mac_db_data():
    columns = ["mac", "name", "switch", "port"]
    search_columns = ["mac", "port"]
    return get_paginated_filtered_sorted_data(db['mac_db'], columns, search_columns=search_columns)


@app.route('/export/mac_db', methods=['GET'])
def export_mac_db_data():
    columns = ["mac", "name", "switch", "port"]
    search_columns = ["mac", "port"]

    data = get_filtered_and_sorted_data_for_export(db['mac_db'], columns, search_columns=search_columns)

    df = pd.DataFrame(data['data'])

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="MAC Data")

    output.seek(0)

    return send_file(output, as_attachment=True, download_name="mac_db_filtered.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == '__main__':
    app.run(debug=True)
