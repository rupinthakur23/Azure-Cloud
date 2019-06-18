# from flask import Flask
from flask import Flask, request, render_template
import pyodbc as db
import time
import random
import redis

app = Flask(__name__)
conn=db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:rupinthakur23.database.windows.net,"
                "1433;Database=earth;Uid=rupin@rupinthakur23;Pwd=Kanu1484@23;Encrypt=yes;TrustServerCertificate=no;"
                "Connection Timeout=30;")
redis_connect_dict = {}
redis_connect_dict['host'] = 'rupin.redis.cache.windows.net'
redis_connect_dict['port'] = 6380
redis_connect_dict['db'] = 0
redis_connect_dict['password'] = 'EU0UzYH8FYlF1mnEX+NSUsk1xh1FDVemL2vrassLxBc='
r = redis.StrictRedis(redis_connect_dict['host'],
                      redis_connect_dict['port'],
                      redis_connect_dict['db'],
                      redis_connect_dict['password'],
                      ssl=True)
def redis_query(query):
    if r.get(query) == None:
        cursor = conn.cursor()
        rcount = cursor.execute(query).fetchall()
        r.set(query, rcount[0][0])
        return None
    else:
        rcount= r.get(query)
        return rcount
@app.route('/')
def hello_world():

    return render_template('common.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

@app.route('/question1', methods=['GET'])
def query_db():
    return render_template('question1.html', )

@app.route('/question1_execute', methods=['GET'])
def query_db_execute():
    mag = request.args.get('mag')
    oper = request.args.get('oper')
    total_time=0


    try:
        # if mag != '' and oper != '':
        # sql = '''SELECT COUNT(*) FROM QUIZ2TABLE where "mag" < ? '''
        #         # cursor.execute(sql, (mag,))
        sql = "SELECT COUNT(*) FROM earthquake.quakes where mag " + oper + mag
        if request.args.get('form') == 'no':
            startTime = time.perf_counter()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            endTime = time.perf_counter()
            result = result[0][0]
            total_time = endTime-startTime
        elif request.args.get('form') == 'yes':
            startTime = time.perf_counter()
            result = redis_query(sql)
            endTime = time.perf_counter()
            if result != None:
                result = str(result)
                result = result.replace("'", '')
                result = result.split('b')
                result = result[-1]
            total_time = endTime - startTime

    except:
        result = "error try again"
    # finally:
    #     conn.close()
    return render_template('question1.html', result=result, total_time=total_time)


@app.route('/question2', methods=['GET'])
def query_db_2():
    return render_template('question2.html', )


@app.route('/question2_execute', methods=['GET'])
def query_db_2_execute():
    qcount = request.args.get('qcount')
    qcount = int(qcount)
    lmag = float(request.args.get('lmag'))
    hmag = float(request.args.get('hmag'))
    rows = []

    total_time=0

    try:
        if request.args.get('form') == 'no':
            startTime = time.perf_counter()
            while qcount != 0:
                sql = "SELECT * FROM earthquake.quakes where mag>3.5"
                cursor = conn.cursor()
                rows = cursor.execute(sql).fetchall()
                print(rows)
                qcount = qcount - 1
            endTime = time.perf_counter()
            total_time = endTime - startTime






        elif request.args.get('form') == 'yes':
            startTime = time.perf_counter()
            sql = "SELECT COUNT(*) FROM earthquake.quakes where mag =" + str(round(random.uniform(lmag, hmag), 1))
            result = redis_query(sql)
            endTime = time.perf_counter()
            if result != None:
                result = str(result)
                result = result.replace("'", '')
                result = result.split('b')
                result = result[-1]
            total_time = endTime - startTime



    except:
        result = "error try again"
    return render_template('question2.html', total_time=total_time, data=rows)

@app.route('/location', methods=['GET'])
def query_db_l():
    return render_template('location.html', )


@app.route('/location_execute', methods=['GET'])
def query_db_l_execute():
    qcount = request.args.get('qcount')
    qcount = int(qcount)
    place = (request.args.get('place'))

    try:
        if request.args.get('form') == 'no':
            startTime = time.perf_counter()
            while qcount != 0:
                sql = "SELECT * FROM earthquake.quakes where place LIKE '%place%' "
                cursor = conn.cursor()
                result = cursor.execute(sql).fetchall()
                qcount = qcount - 1
            endTime = time.perf_counter()
            total_time = endTime - startTime
        elif request.args.get('form') == 'yes':
            startTime = time.perf_counter()
            sql = "SELECT COUNT(*) FROM earthquake.quakes where place LIKE '%place%' "
            result = redis_query(sql)
            endTime = time.perf_counter()
            if result != None:
                result = str(result)
                result = result.replace("'", '')
                result = result.split('b')
                result = result[-1]
            total_time = endTime - startTime


    except:
        result = "error try again"
    return render_template('location.html', total_time=total_time)

@app.route('/question3', methods=['GET'])
def query_db_23():
    return render_template('question3.html', )


@app.route('/question3_execute', methods=['GET'])
def query_db_23_execute():
    qcount = request.args.get('qcount')
    qcount = int(qcount)
    lmag =request.args.get('lmag')
    hmag = request.args.get('hmag')
    sdate = request.args.get('sdate')
    edate= request.args.get('edate')
    print(lmag)
    print(hmag)
    total_time=0

    try:
        if request.args.get('form') == 'no':
            startTime = time.perf_counter()
            print(startTime)

            while qcount != 0:
                sql = "SELECT COUNT(*) FROM earthquake.quakes where mag >"+ lmag+ " and mag<" + hmag

                cursor = conn.cursor()
                result = cursor.execute(sql).fetchall()
                qcount = qcount - 1
            endTime = time.perf_counter()
            total_time = endTime - startTime
        elif request.args.get('form') == 'yes':
            startTime = time.perf_counter()
            sql = "SELECT COUNT(*) FROM earthquake.quakes where mag >"+ lmag+ " and mag<" + hmag
            result = redis_query(sql)
            endTime = time.perf_counter()
            if result != None:
                result = str(result)
                result = result.replace("'", '')
                result = result.split('b')
                result = result[-1]
            total_time = endTime - startTime

    except:
        result = "error try again"
    return render_template('question3.html', total_time=total_time)




if __name__ == '__main__':
  app.run()