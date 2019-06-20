# from flask import Flask
from flask import Flask, request, render_template
import pyodbc as db
import pygal
import time
import random

app = Flask(__name__)
conn=db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:rupinthakur23.database.windows.net,"
                "1433;Database=earth;Uid=rupin@rupinthakur23;Pwd=Kanu1484@23;Encrypt=yes;TrustServerCertificate=no;"
                "Connection Timeout=30;")


@app.route('/')
def hello_world():
    return render_template('common.html',)



@app.route('/question1', )
def question1():
    return render_template('question1.html')

@app.route('/question1_execute',  methods=['GET'])
def question1_execute():
    bar_chart = pygal.Bar(width=1000, height=500)
    sql = "select * from earthquake.population where convert(varchar,State) = 'Alabama' or convert(varchar,State) = 'Alaska' or convert(varchar,State) = 'California' or convert(varchar,State) = 'Florida'"
    print(sql)
    cursor = conn.cursor()
    result = cursor.execute(sql).fetchall()
    #population_values = []
    for r in result:
        state = r[0]
        population_values = []
        for year in range(1,len(r)):
            string_val = r[year]

            int_val = int(string_val)
            population_values.append(int_val)
        bar_chart.add(state, population_values)
    return render_template('question1.html', chart=bar_chart.render_data_uri())

@app.route('/question2', )
def question2():
    return render_template('question2.html')

@app.route('/question2_execute',  methods=['GET'])
def question2_execute():
    cursor = conn.cursor()
    sql = "select * from earthquake.population where convert(varchar,State) = 'Alabama' or convert(varchar,State) = 'Florida'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    xy_chart = pygal.XY(stroke=False, height=300)
    xy_chart.title = 'Correlation'
    for r in result:
        db_years = [None, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
        state = ""
        scatterplot_data = []
        for i in range(1, len(r)):
            state = r[0]
            print(r[0])
            population_val = r[i]
            print(r[i])

            int_val = int(population_val)
            tuple = (db_years[i], int_val)
            scatterplot_data.append(tuple)
        xy_chart.add(state, scatterplot_data)
    xy_chart.render()
    return render_template('question2.html', chart=xy_chart.render_data_uri())
    #return render_template('question2.html', result=result, chart=bar_chart.render_data_uri(), line =line.render_data_uri() )

@app.route('/question3', )
def question3():
    return render_template('question3.html')


@app.route('/question3_execute',  methods=['GET'])
def question3_execute():
    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    pie_chart.render()
    return render_template('question3.html', chart=pie_chart.render_data_uri())

@app.route('/question4', )
def question7():
    return render_template('question4.html')

@app.route('/question4_execute',  methods=['GET'])
def question7_execute():
    bar_chart = pygal.Bar(width=1000, height=500)
    year = str(request.args.get('year'))


    # year = 'y_'+year
    lrange1 = request.args.get('lrange1')
    hrange1 = request.args.get('hrange1')
    lrange2 = request.args.get('lrange2')
    hrange2 = request.args.get('hrange2')
    lrange3 = request.args.get('lrange3')
    hrange3 = request.args.get('hrange3')
    range = [lrange1 +'-' + hrange1, lrange2 +'-' + hrange2, lrange3 +'-' + hrange3]
    print(range)
    cursor = conn.cursor()
    sql = "select count(*) from earthquake.population where [" + year + "]between " + "'" + lrange1 + "'" + " and " + "'" + hrange1 + "'"
    sql1 = "select count(*) from earthquake.population where [" + year + "] between " + "'" + lrange2 + "'" + " and " + "'" + hrange2 + "'"
    sql2 = "select count(*) from earthquake.population where [" + year + "] between " + "'" + lrange3 + "'" + " and " + "'" + hrange3 + "'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    print(result)
    answers = []
    answers.append(result[0][0])
    result = cursor.execute(sql1).fetchall()
    answers.append(result[0][0])
    result = cursor.execute(sql2).fetchall()
    answers.append(result[0][0])
    bar_chart.add(range[0], answers[0])
    bar_chart.add(range[1], answers[1])
    bar_chart.add(range[2], answers[2])
    return render_template('question4.html', chart=bar_chart.render_data_uri())


@app.route('/question5', )
def question10():
    return render_template('question5.html')

@app.route('/question5_execute',  methods=['GET'])
def question10_execute():
    range = int(request.args.get('range'))

    bar_chart = pygal.Bar(width=1000, height=500)
    year = str(request.args.get('year'))

    print(year)
    lrange1 = 0
    hrange1 = lrange1 + range
    lrange2 = hrange1
    hrange2 = hrange1 + range
    lrange3 = hrange2
    hrange3 = hrange2 + range
    range = [str(lrange1) +'-' + str(hrange1), str(lrange2) +'-' + str(hrange2), str(lrange3) +'-' + str(hrange3)]
    print(range)
    cursor = conn.cursor()
    sql = "select count(*) from earthquake.population where [" + year + "] between " + "'" + str(lrange1) + "'" + " and " + "'" + str(hrange1) + "'"
    sql1 = "select count(*) from earthquake.population where [" + year + "] between " + "'" + str(lrange2) + "'" + " and " + "'" + str(hrange2) + "'"
    sql2 = "select count(*) from earthquake.population where [" + year + "]between " + "'" + str(lrange3) + "'" + " and " + "'" + str(hrange3) + "'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    print(result)
    answers = []
    answers.append(result[0][0])
    result = cursor.execute(sql1).fetchall()
    answers.append(result[0][0])
    result = cursor.execute(sql2).fetchall()
    answers.append(result[0][0])
    bar_chart.add(range[0], answers[0])
    bar_chart.add(range[1], answers[1])
    bar_chart.add(range[2], answers[2])
    return render_template('question5.html', chart=bar_chart.render_data_uri())


@app.route('/question6', )
def question101():
    return render_template('question6.html')


@app.route('/question6_execute',  methods=['GET'])
def question101_execute():

    rows=[]
    cursor = conn.cursor()
    sql = "Select StateName from earthquake.voting where convert(varchar, TotalPop) >'5000' or convert(varchar,TotalPop) <'10000'"

    result = cursor.execute(sql).fetchall()

    return render_template('question6.html',data=result)

@app.route('/question7', )
def question1011():
    return render_template('question7.html')


@app.route('/question7_execute',  methods=['GET'])
def question1011_execute():

    rows=[]
    cursor = conn.cursor()
    sql = "Select StateName from earthquake.voting where convert(varchar, TotalPop) >'10000' or convert(varchar,TotalPop) <'40000'"

    result = cursor.execute(sql).fetchall()

    return render_template('question7.html',data=result)

if __name__ == '__main__':
  app.run()