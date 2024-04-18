import pymysql
import math

ENDPOINT = 'gt7race-randomizer-instance-1.cxw462gwsmti.us-east-1.rds.amazonaws.com'
USERNAME = 'gtadmin'
PASSWORD = 'gtgamegenerator'
DATABASE_NAME = 'gran_turismo_generator'


def lambda_handler(event,context):
    try :
        connection = pymysql.connect(host = ENDPOINT, user = USERNAME, passwd = PASSWORD, db = DATABASE_NAME)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # retrieve number of laps and tracks wanted
            numOfTracks = int(event['numRaces'])
            raceFormat = int(event['raceFormat'])  
            
            # query to get course name, layout, and length(to figure laps)
            track_query = "SELECT id, course_name, layout, length_meters FROM RaceTracks ORDER BY RAND() LIMIT %s"
            cursor.execute(track_query, (numOfTracks,)) 
            results = cursor.fetchall()
            
            # for each track, figure out number of laps and attach it to the dictionary for each track 
            for result in results:
                numOfLaps = math.ceil(raceFormat/ result['length_meters'])
                result['num_of_laps'] = numOfLaps
                print(result)
            
    except pymysql.MySQLError as e: 
        print("ERROR: Could not connect to MySQL instance")
        print(e)
    
    finally:
        if connection:
            connection.close()


    
    


