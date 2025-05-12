import pymysql
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

conn = pymysql.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    database=config['mysql']['database'],
    charset='utf8',
    autocommit=True
)

def save_result(category, content):
    with conn.cursor() as cursor:
        sql = "INSERT INTO check_results (category, content) VALUES (%s, %s)"
        cursor.execute(sql, (category, content))
