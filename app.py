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

if __name__ == '__main__':
  app.run()