import mysql.connector
from datetime import datetime
from datetime import timedelta


def score_it(successful_commits):
    return successful_commits * 2

def evaluate_it_for_date(date_to_check):
    date_str = date_to_check.strftime("%Y-%m-%d")


    conn = mysql.connector.connect(
        host="3.108.53.187",
        user="aditya",
        password="aditya123"
    )
    cursor = conn.cursor(dictionary=True)
    insert_cursor = conn.cursor()

    #  Count successful commits
    cursor.execute("""
        SELECT COUNT(*) AS success_count 
        FROM website.github_commit
        WHERE DATE(last_commit_time) = %s AND status = 'success'
    """, (date_str,))
    result = cursor.fetchone()

    if result and result["success_count"] > 0:
        count = result["success_count"]
        points = score_it(count)

        #  Insert
        insert_cursor.execute("""
            INSERT INTO hack.it_employee_1_points (record_date, points)
            VALUES (%s, %s)
        """, (date_str, points))

        conn.commit()
        print(f"✅ Sugar Ducky points for {date_str}: {points} for {count} successful commits")
    else:
        print(f"⚠️ No successful commits found man , work hard and try commit to git and work as balance is important{date_str}")

    cursor.close()
    insert_cursor.close()
    conn.close()


# evaluate_it_for_date(datetime.strptime("2025-03-03", "%Y-%m-%d"))


start_date = datetime.strptime("2025-03-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-03-10", "%Y-%m-%d")

current_date = start_date
while current_date <= end_date:
    evaluate_it_for_date(current_date)
    current_date += timedelta(days=1)
