import time

import clickhouse_connect
import datetime
from random import randint

number_of_services = 42
number_of_departments = 278
# ------------------------- Clickhouse -------------------------
client = clickhouse_connect.get_client(host='localhost', port="8123", username="flints", password="moreflints")

# c1 = "CREATE TABLE clients (datetime TIMESTAMP, department_id INT, "
# c2 = ''
# for i in range(42):
#     c2 += f"service_{i} INT, "
# c3 = ") ENGINE MergeTree ORDER BY datetime"
# client.command(c1 + c2[:-2] + c3)

data = []
for department_id in range(number_of_departments):
    row = [datetime.datetime.now(), department_id]
    for i in range(number_of_services):
        row.append(randint(1, 10))
    data.append(row)
column_names = ["datetime", "department_id"]
for i in range(number_of_services):
    column_names.append(f"service_{i}")
client.insert("clients", data, column_names=column_names)

result = client.query("SELECT * FROM clients")
