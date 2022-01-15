import functools
from datetime import date, datetime
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask import Flask, render_template, request
from werkzeug.exceptions import abort
import sqlite3 as sql
from calc_app.db import get_db


#app = Flask(__name__)
#app.config.from_object(__name__)

bp = Blueprint('calc', __name__)

@bp.route('/')
def index():
    #db = get_db()
    #posts = db.execute('SELECT * FROM quote')
    return render_template('form.html')


@bp.route('/result1', methods=['POST'])
def result1():

    var_4 = request.form.get("var_4", type=str)
    var_3 = request.form.get("var_3", type=str)
    var_2 = request.form.get("var_2", type=str)
    var_1 = request.form.get("var_1", type=str)
    operation = request.form.get("operation")


    if(operation == 'Get Quote'):
        tester = transform(var_1)
        computed_age = age(tester)
        monthly_premium = premium_per_month(computed_age)
        six_month_premium = six_month_quote(monthly_premium)
        result = six_month_premium
        db = get_db()
        error = None
        #quote_id = 0

        if not var_4:
            error = 'First Name is required.'
        elif not var_3:
            error = 'Last Name is required.'
        elif not var_2:
            error = "ZIP Code is required."
        elif not var_1:
            error = "Date Of Birth is required."
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (fname, lname, ZIP, DOB, quote) VALUES (?, ?, ?, ?, ?)",
                    (var_4, var_3, var_2, var_1, six_month_premium),)
                db.commit()
                db.execute(
                    "INSERT INTO quote (user_id, six_month_quote) VALUES ((SELECT id FROM user ORDER BY id DESC LIMIT 1), ?)",
                    (six_month_premium,),)
                db.commit()
                #quote_id = db.execute("SELECT id FROM quote ORDER BY id DESC LIMIT 1")

            except db.IntegrityError:
                error = f"User {var_4} is already registered."
            # else:
            # return redirect(url_for("index"))
        flash(error)
    elif (operation == 'Lookup Quote'):
        return redirect(url_for('calc.result2'))
    elif (operation == 'Display Quotes Issued in the Last 24 Hours'):
        return redirect(url_for('calc.result3'))

        #result = 1

        #return render_template('result2.html', entry=result)
        #result = query_db('SELECT * FROM quote')

    else:
        result = 'INVALID CHOICE'
    entry = result

    #quote_id = db.execute('SELECT id FROM quote ORDER BY id DESC LIMIT 1',)
    #newentry = quote_id
    return render_template('result1.html', entry=entry)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def transform(birthday):

    date_object = datetime.strptime(birthday, "%Y-%m-%d").date()
    return date_object

def age(birthdate):

    today = date.today()
    one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))
    year_difference = today.year - birthdate.year
    age = year_difference - one_or_zero
    return age


def premium_per_month(age):
    prem = 600 + 0.3 * (abs(age-50))**1.5
    return prem

def six_month_quote(monthly_premium):
    return monthly_premium * 6







@bp.route('/result2', methods=['GET'])
def result2():
    db = get_db()
    con = sql.connect("calc_app.db")
    con.row_factory = sql.Row
    var_4 = request.form.get("var_4", type=str)
    var_3 = request.form.get("var_3", type=str)
    var_2 = request.form.get("var_2", type=str)
    var_1 = request.form.get("var_1", type=str)

    cur = con.cursor()
    quotes = db.execute("select quote from user where fname = ? AND lname = ?", (var_4, var_3)).fetchone()

    return render_template("result2.html", rows=quotes)





@bp.route('/result3', methods=['GET'])
def result3():
    db = get_db()
    quotes = db.execute("select * from quote where created >= datetime('now','-1 day')").fetchall()
    return render_template("viewall.html", rows=quotes)


@bp.route('/result4', methods=['GET'])
def result4():
    db = get_db()
    con = sql.connect("calc_app.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    quotes = db.execute("select * from quote where created >= datetime('now','-1 day')").fetchall()

    return render_template("viewall.html", rows=quotes)

    #db = get_db()
    #db.row_factory = sql.Row
    #cur = db.cursor()
    #rows = cur.execute("select * from quote").fetchall()
    #entry = rows
    #return render_template('viewall.html', entry=entry)

    #if(operation == 'Display Quotes Issued in the Last 24 Hours'):
        #post = get_db().execute('SELECT * FROM quote ').fetchone()

        #if post is None:
            #abort(404, f"Post id {id} doesn't exist.")
    #return post

        #if check_author and post['author_id'] != g.user['id']:
            #abort(403)

#if __name__ == '__main__':
    #app.run(debug=True)
