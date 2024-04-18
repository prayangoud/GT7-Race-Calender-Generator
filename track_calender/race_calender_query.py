import pymysql
import math
import json
import boto3
from botocore.exceptions import ClientError

#AWS Secrets Manager
secret_name = "GTGenDB"
region_name = "us-east-1"

session = boto3.session.Session()
client = session.client(service_name = 'secretsmanager', region_name = region_name)

def lambda_handler(event,context):
    connection = None
    try :
        #get secret
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        secret = json.loads(secret)
        
        #connect to database
        connection = pymysql.connect(host = secret['host'], user = secret['username'], passwd = secret['password'], db = secret['dbname'])
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # retrieve number of laps, tracks, and car type wanted
            numOfTracks = int(event['numRaces'])
            raceFormat = int(event['raceFormat'])
            car_category = str(event['carType'])  
            
            # query to get course name, layout, and length(to figure laps)
            track_query = "SELECT id, course_name, layout, length_meters FROM RaceTracks ORDER BY RAND() LIMIT %s"
            cursor.execute(track_query, (numOfTracks,)) 
            track_results = cursor.fetchall()

            # query to get cars that fit specification
            car_query = "SELECT car_id, car, brand, category FROM CarList WHERE category = %s;"
            cursor.execute(car_query, (car_category,))
            car_results = cursor.fetchall()
            
            # for each track, figure out number of laps and attach it to the dictionary for each track 
            for track in track_results:
                numOfLaps = math.ceil(raceFormat/ track['length_meters'])
                track['num_of_laps'] = numOfLaps


            race_data = {
                'tracks': track_results,
                'cars': car_results
                }
            return{
                'statusCode' : 200,
                'body':json.dumps(race_data)
            }
            
    except pymysql.MySQLError as e: 
        print("ERROR: Could not connect to MySQL instance", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        
    except Exception as e:
        print("ERROR: An unexpected error occurred:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
    finally:
        # close connection
        if connection:
            connection.close()
