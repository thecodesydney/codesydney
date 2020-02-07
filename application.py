from flask import Flask, render_template, g, request, session, redirect, url_for
import sqlite3
from os import path

application = Flask(__name__)

#Database helper
ROOT = path.dirname(path.realpath(__file__))
def connect_db():
    sql = sqlite3.connect(path.join(ROOT, "talent.db"))
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@application.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()
    return_values = []
    if request.method == 'POST':
        search_keywords = request.form['search']
        if search_keywords:
            keywords = search_keywords + '*'
            details_cur = db.execute('SELECT ID, Name, Role, Projects, Certifications FROM talentsearch WHERE talentsearch MATCH ?', [keywords])                              
        else:
            details_cur = db.execute('SELECT ID, Name, Role, Projects, Certifications FROM talentsearch')            
    else:
        db = get_db()
        details_cur = db.execute('SELECT ID, Name, Role, Projects, Certifications FROM talentsearch')                              
        
    details = details_cur.fetchall()
    for detail in details:
        detail_dict = {}
        detail_dict['ID'] = detail['ID']
        detail_dict['Name'] = detail['Name']
        detail_dict['Role'] = detail['Role']
        detail_dict['Projects'] = detail['Projects']
        detail_dict['Certifications'] = detail['Certifications']        
        return_values.append(detail_dict)      
        
    return render_template('index.html', return_values=return_values)
    
if __name__ == '__main__':
    application.run(debug=True)