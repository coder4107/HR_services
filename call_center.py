import mysql.connector
from datetime import datetime
from datetime import timedelta

def score_call_center(calls, satisfaction):
    score = calls // 10
    if satisfaction >= 4.0:
        score += 2
    return score

def evaluate_call_center_for_date(date_to_check):
    date_str = date_to_check.strftime("%Y-%m-%d")


    conn = mysql.connector.connect(
        host="3.108.53.187",
        user="aditya",
        password="aditya123"
    )
    cursor = conn.cursor(dictionary=True)
    insert_cursor = conn.cursor()

    # Fetch data
    cursor.execute("SELECT * FROM website.call_statistics WHERE call_date = %s", (date_str,))
    row = cursor.fetchone()

    if row:
        calls = row["number_of_calls"]
        satisfaction = row["avg_satisfaction_rate"]
        points = score_call_center(calls, satisfaction)

        #  Insert
        insert_cursor.execute("""
            INSERT INTO hack.call_employee_1_points (record_date, points)
            VALUES (%s, %s)
        """, (date_str, points))

        conn.commit()
        print(f"✅ Sugar Ducky points for {date_str}: {points} points (calls: {calls})")
    else:
        print(f"⚠️ No call data found for , were you sleeping on the job  {date_str}")

    cursor.close()
    insert_cursor.close()
    conn.close()


# evaluate_call_center_for_date(datetime.strptime("2025-03-03", "%Y-%m-%d"))


start_date = datetime.strptime("2025-03-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-03-10", "%Y-%m-%d")

current_date = start_date
while current_date <= end_date:
    evaluate_call_center_for_date(current_date)
    current_date += timedelta(days=1)