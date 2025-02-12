import pymysql

def get_all_pages_from_database(appType):
    conn = pymysql.connect(host='10.101.252.43',
                           port=5002,
                           user='powerful',
                           password='powerful',
                           database='banma_powerful_performance',
                           connect_timeout=60)
    print("Database connection successful.")
    while True:
        try:
            cursor = conn.cursor()
            # sql = "SELECT COUNT(*) FROM banma_powerful_performance.banma_key_pages"
            sql = "SELECT * FROM banma_powerful_performance.banma_key_pages where app_type = {appType}".format(appType = appType)
            cursor.execute(sql)
            results = cursor.fetchall()

            # print(results)
            print("The database processing is complete.")
            conn.close()
            break
        except Exception as error:
            conn.ping(True)
    return results






