from flask import Flask,request,redirect
import sqlite3
import shortuuid

app = Flask(__name__) # Initialize Flask app

conn=sqlite3.connect("urlDB.db",check_same_thread=False) # Connect to sqlite3 Database

conn.execute('''CREATE TABLE IF NOT EXISTS urls
         (longUrl TEXT UNIQUE NOT NULL, 
          shortUrl TEXT UNIQUE NOT NULL);''')

@app.route("/shorten")                      # Route to which the URL to shorten is sent
def shorten():
    print(request.url_root)
    cur=conn.cursor()
    long_url=request.args.get('url')
    short_url=request.url_root+shortuuid.uuid()
    try:   
        cur.execute("INSERT INTO urls VALUES (?,?)",(long_url,short_url))
        conn.commit()
        return short_url,200
    except:
        return "Duplicate Error" ,500

@app.route("/<code>")                           # Route handling redirection of new shortened URL
def map(code):
    cur=conn.cursor()
    url_to_find=request.url_root+code
    try:
        cur.execute("SELECT longUrl FROM urls WHERE shortUrl=?",(url_to_find,))
        row=cur.fetchone()
        return redirect(row[0],code=302)
    except:
        return "URL not found",500


if __name__ == "__main__":
    app.run()
