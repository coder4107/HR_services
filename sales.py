import mysql.connector
from datetime import datetime
from datetime import timedelta


def score_sales(target, finished):
    if target == 0:
        return 0
    ratio = finished / target
    if ratio >= 1:
        return 5
    elif ratio >= 0.95:
        return 3
    elif ratio >= 0.90:
        return 2
    else:
        return 1

def evaluate_sales_for_date(date_to_check):
    date_str = date_to_check.strftime("%Y-%m-%d")


    conn = mysql.connector.connect(
        host="3.108.53.187",
        user="aditya",
        password="aditya123"
    )
    cursor = conn.cursor(dictionary=True)
    insert_cursor = conn.cursor()

    #  Fetch sales
    cursor.execute("SELECT * FROM website.sales WHERE sale_date = %s", (date_str,))
    data = cursor.fetchone()

    if data:
        target = data["target"]
        finished = data["target_finished"]
        points = score_sales(target, finished)

        #  Insert
        insert_cursor.execute("""
            INSERT INTO hack.sales_employee_1_points (record_date, points)
            VALUES (%s, %s)
        """, (date_str, points))

        conn.commit()
        print(f"✅ Sugar Duckys score for {date_str} is  {points} ")
    else:
        print(f"⚠️ No sales data found for {date_str}")

    cursor.close()
    insert_cursor.close()
    conn.close()

# evaluate_sales_for_date(datetime.strptime("2025-03-03", "%Y-%m-%d"))



start_date = datetime.strptime("2025-03-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-03-10", "%Y-%m-%d")

current_date = start_date
while current_date <= end_date:
    evaluate_sales_for_date(current_date)
    current_date += timedelta(days=1)