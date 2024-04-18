import json
import pymysql

ENDPOINT = 'gt7race-randomizer-instance-1.cxw462gwsmti.us-east-1.rds.amazonaws.com'
USERNAME = 'gtadmin'
PASSWORD = 'gtgamegenerator'
DATABASE_NAME = 'gran_turismo_generator'

connection = pymysql.connect(host = ENDPOINT, user = USERNAME, passwd = PASSWORD, db = DATABASE_NAME)

def lambda_handler(event,context):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    car_category = event['category']
    
    #get car models
    car_query = "SELECT car_id, car, brand, category FROM CarList WHERE category = %s;"

    cursor.execute(car_query, (car_category,))
    
    results = cursor.fetchall()

    for result in results:
        print(result)
    
    
    cursor.close()
    connection.close()


