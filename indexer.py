from flask import Flask, render_template, g, request, session, redirect, url_for
import sqlite3
from os import path

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

db = get_db()
details_cur = db.execute('CREATE VIRTUAL TABLE talentsearch USING fts5(ID, Name, Role, Projects, Certifications)')
details_cur = db.execute('INSERT INTO talentsearch SELECT ID, Name, Role, Projects, Certifications FROM talent')