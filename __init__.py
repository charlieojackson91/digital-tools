from flask import Flask, render_template, flash, request, url_for, redirect, session
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from flask_mail import Mail, Message
import os
import time

# Word to html converter
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

# Language processer
from language_processing import categorise_speech,classify_keywords

# My content management system
from content_management import Content, Articles,Tools

# Connect to db
from dbconnect import connection, add_project

# Crawler
from crawler import Crawl_url,Get_rankings, Get_uat

# Compare strings, check cannibalisation
from similar import how_similar, canni_check


app = Flask(__name__)

# Mailing configuration
app.config.update(
	DEBUG=True, # change to false in production
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'charlieojackson@gmail.com',
	MAIL_PASSWORD = 'INPUT PASSWORD'
	)
mail = Mail(app)


# Send test email - to run this code you must allow access to google with less secure apps - https://support.google.com/accounts/answer/6010255?hl=en 
@app.route('/send-mail/')
def send_mail():
	try:
		msg = Message("Send Mail Tutorial!",
                sender="charlieojackson@gmail.com",
                recipients=["charlie@meltcontent.com"])
		msg.body = "Yo!\nHave you heard the good word of Python???"           
		mail.send(msg)
		return 'Mail sent!'
	except Exception, e:
		return(str(e)) 


FREE_TOOLS = Content()
ARTICLE_DICT = Articles()
PAID_TOOLS = Tools()


#ROBOTS TXT
@app.route("/robots.txt")
def robots_txt():
    return render_template('robots.txt')

# HOMEPAGE
@app.route("/")
def homepage():
    return render_template('homepage.html')


# Sign in
@app.route("/sign-in",methods=["GET","POST"])
def sign_in():
    try:
        if request.method == "POST":
            c, conn = connection()
            email = request.form['email']
            password = request.form['password']
            c.execute("SELECT * FROM Users WHERE email = %s;",(thwart(email),))
            try:
                data = c.fetchone()
                login = data[2]
                username = data[1]
                user_id = data[0]
                if sha256_crypt.verify(password, login):
                    session['logged_in'] = True
                    session['username'] = username
                    session['user_id'] = user_id
                    flash('You are now logged in')
                    return redirect(url_for("seo_tools"))
                else:
                    error = "The email or password is wrong"
                    return render_template('sign-in.html',error = error)
            except:
                error = "The email or password is wrong"
                return render_template('sign-in.html',error = error)   
        else:
            return render_template('sign-in.html')
    except Exception as e:
        flash(e)
        return render_template('sign-in.html')

# Register page
@app.route("/register",methods=["GET","POST"])
def register():
    try:
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            password = sha256_crypt.encrypt(str(request.form['password']))
            c, conn = connection()
            x = c.execute("SELECT * FROM Users WHERE username = %s;",(thwart(username),))
            y = c.execute("SELECT * FROM Users WHERE email = %s;",(thwart(email),))
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return redirect(url_for('register'))
            if int(y) > 0:
                flash("That email is already registered - please sign in")
                return redirect(url_for('sign_in'))
            else:
                c.execute("INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)",(thwart(username), thwart(password), thwart(email)))
                conn.commit()
                flash("Thanks for registering! Please make use of all the available tools")
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('seo_tools'))
            return render_template('register.html')
        else:
            return render_template('register.html')
    except Exception as e:
        flash(e)
        return render_template('register.html')


# Logout
@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('working', None)
    session.pop('projects', None)
    return redirect(url_for('seo_tools'))


# Contact page
@app.route("/contact",methods=["GET","POST"])
def contact():
    return render_template('contact.html')

# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('four-oh-four.html')

# FREE SEO tools
@app.route('/seo-tools')
def seo_tools():
    try:
        if session.get('logged_in') == True:
            return render_template('seo-tools.html',FREE_TOOLS = FREE_TOOLS,PAID_TOOLS=PAID_TOOLS)
        else:
            return render_template('seo-tools.html',FREE_TOOLS = FREE_TOOLS)
    except Exception as e:
        flash(e)
        return render_template('seo-tools.html',FREE_TOOLS = FREE_TOOLS)

# Python Tutorials
@app.route('/programming-tutorials')
def programming_tutorials():
    return render_template('programming-tutorials.html')

# Knowledge hub
@app.route('/knowlegde-hub')
def knowledge_hub():
    return render_template('knowledge-hub.html')


# Merge words tool
@app.route('/seo-tools/merge-words')
def merge_words_tool():
    return render_template('tools/merge-words-tool.html')

# Merge words tutorial
@app.route('/python-tutorials/merge-words')
def merge_words_tutorial():
    return render_template('tutorials/merge-words-tutorial.html',ARTICLE_DICT = ARTICLE_DICT)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML to word converter
@app.route('/seo-tools/word-html-converter', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',
                                        filename=filename))
        return render_template('tools/word-to-html.html')
    except Exception as e:
        flash('This tool does not work yet')
        return render_template('tools/word-to-html.html')
    

# Rank tracker
@app.route('/seo-tools/rank-tracker',methods=["GET","POST"])
def rank_tracker():
    try:
        if request.method == "POST":
            keyword = request.form['keyword']
            rankings = Get_rankings(keyword)
            # store in session and then redirect
            session['rankings'] = rankings
            return redirect(url_for('rank_tracker'))
        else:
            try:
                rankings = session['rankings']
                session.pop('rankings', None)
                return render_template('tools/rank-tracker.html',rankings = rankings)
            except:
                return render_template('tools/rank-tracker.html')
    except Exception as e:
        flash(e)
        return render_template('tools/rank-tracker.html')




  
# NLTK tool
@app.route('/seo-tools/keyword-classification-nlp',methods=["GET","POST"])
def nltk_tool():
    try:
        if request.method == "POST":
            keywords = request.form['keywords']
            #nouns, adjectives,verbs = categorise_speech(keywords)
            nouns, adjectives, verbs = categorise_speech(keywords)
            return render_template('tools/nltk.html',nouns = nouns,adjectives = adjectives,verbs = verbs )
        else:
            return render_template('tools/nltk.html')
    except Exception as e:
        flash(e)
        return render_template('tools/nltk.html')



# Keyword classification
@app.route('/seo-tools/keyword-classification',methods=["GET","POST"])
def keyword_classify():
    try:
        if request.method == "POST":
            keyword = request.form['keywords']
            classifiers = request.form['classifiers']
            classify = classify_keywords(keyword,classifiers)
            return render_template('tools/keyword-classification.html',classify = classify)
        else:
            return render_template('tools/keyword-classification.html')

    except Exception as e:
        flash(e)
        return render_template('tools/keyword-classification.html')


# Web scraping tool
@app.route('/seo-tools/web-crawling',methods=["GET","POST"])
def web_scraping_tool():
    try:
        if request.method == "POST":
            url = request.form['keyword']
            if url.startswith('http') == True:
                meta = Crawl_url(url)
                session['meta'] = meta
                return redirect(url_for('web_scraping_tool'))
            else:
                bad_url = "Please enter a valid URL"
                return render_template('tools/web-scraping.html',bad_url = bad_url)
        else:
            try:
                meta = session['meta']
                session.pop('meta', None)
                return render_template('tools/web-scraping.html',meta = meta)
            except:
                return render_template('tools/web-scraping.html')
    except Exception as e:
        flash(e)
        return render_template('tools/web-scraping.html')
    


# UAT, lorem ipsum Tool
@app.route('/seo-tools/uat-finder',methods=["GET","POST"])
def uat_tool():
    try:
        if request.method == "POST":
            url = request.form['url']
            uat = Get_uat(url)
            session['uat'] = uat
            return redirect(url_for('uat_tool'))
        else:
            try:
                uat = session['uat']
                session.pop('uat', None)
                return render_template('tools/uat-finder.html', uat = uat)
            except:
                return render_template('tools/uat-finder.html')
    except Exception as e:
        flash(e)
        return render_template('tools/uat-finder.html')



# Forecasting tool
@app.route('/seo-tools/seo-forecast')
def forecasting_tool():
    return render_template('tools/seo-forecast.html')

# Fuzzy look up tool
@app.route('/seo-tools/fuzzy-look-up',methods=["GET","POST"])
def fuzzy_look_up():
    try:
        if request.method == "POST":
            pre_urls = request.form['pre-urls']
            post_urls = request.form['post-urls']
            try:
                fuzzy = how_similar(pre_urls,post_urls)
                session['fuzzy'] = fuzzy
                return redirect(url_for('fuzzy_look_up'))
            except Exception as e:
                flash(e)
                return render_template('tools/fuzzy.html')
        else:
            try:
                fuzzy = session['fuzzy']
                session.pop('fuzzy', None)
                return render_template('tools/fuzzy.html', fuzzy = fuzzy)
            except:
                return render_template('tools/fuzzy.html')
    except Exception as e:
        flash(e)
        return render_template('tools/fuzzy.html')

# Canni tool
@app.route('/seo-tools/seo-cannibalisation',methods=["GET","POST"])
def canni_tool():
    try:
        if request.method == "POST":
            canni_data = request.form['canni']
            brand_name = request.form['brand']
            cannibalisation = canni_check(canni_data,brand_name)
            return render_template('tools/canni-tool.html', cannibalisation = cannibalisation)
        else:
            test = "hit else"
            return render_template('tools/canni-tool.html',test = test)
    except Exception as e:
        flash(e)
        return render_template('tools/canni-tool.html')

# JS crawler
@app.route('/seo-tools/js-crawler',methods=["GET","POST"])
def js_crawler():
    try:
        if request.method == "POST":
            url = request.form['url']
            jscrawl = url # THIS CODE NEEDS COMPLETING - i think this is running on python2 and library is in python3
            return render_template('tools/js-crawler.html',jscrawl = jscrawl)
        else:
            return render_template('tools/js-crawler.html')
    except Exception as e:
        flash(e)
        return render_template('tools/js-crawler.html')


# Rank tracker - PAID
@app.route('/seo-tools/ultimate-rank-tracker',methods=["GET","POST"])
def rank_tracker_ultimate():
    try:
        c, conn = connection()
        user_id = session['user_id']
        if session.get('logged_in') == True:
            projects = c.execute('SELECT DISTINCT Projects.project_id,Projects.client_name,Projects.domain FROM Projects JOIN Keywords JOIN Users ON Projects.project_id = Keywords.project_id AND Users.user_id = Keywords.user_id WHERE Keywords.user_id = %s;',(str(user_id),))
            data = c.fetchall()
            session['projects'] = data
            #session['working'] = data[0]
            #project_id = session['working']
            if request.method == "GET":
                try:
                    project_id = request.args.get('project_id')
                    c.execute('SELECT Keywords.key_id,Keywords.keyword, Keywords.search_volume, Keywords.competition,Keywords.tag,Keywords.project_id FROM Keywords JOIN Users JOIN Projects ON Projects.project_id = Keywords.project_id AND Users.user_id = Keywords.user_id WHERE Users.user_id = %s AND Projects.project_id = %s;',(str(user_id),thwart(project_id),))
                    keyword_set = c.fetchall()
                    url = request.url
                    session['working'] = project_id
                    return render_template('paid-tools/rank-tracker-ultimate.html', keyword_set = keyword_set,project_id = project_id)
                except:
                    try:
                        project_id = session['working']
                        c.execute('SELECT Keywords.key_id,Keywords.keyword, Keywords.search_volume, Keywords.competition,Keywords.tag,Keywords.project_id FROM Keywords JOIN Users JOIN Projects ON Projects.project_id = Keywords.project_id AND Users.user_id = Keywords.user_id WHERE Users.user_id = %s AND Projects.project_id = %s;',(str(user_id),thwart(project_id),))
                        keyword_set = c.fetchall()
                        return render_template('paid-tools/rank-tracker-ultimate.html',keyword_set = keyword_set)
                    except:
                        project_id = "1"
                        c.execute('SELECT Keywords.key_id,Keywords.keyword, Keywords.search_volume, Keywords.competition,Keywords.tag,Keywords.project_id FROM Keywords JOIN Users JOIN Projects ON Projects.project_id = Keywords.project_id AND Users.user_id = Keywords.user_id WHERE Users.user_id = %s AND Projects.project_id = %s;',(str(user_id),thwart(project_id),))
                        keyword_set = c.fetchall()
                        return render_template('paid-tools/rank-tracker-ultimate.html',keyword_set = keyword_set)
            else:
                project_id = session['working']
                c.execute('SELECT Keywords.key_id,Keywords.keyword, Keywords.search_volume, Keywords.competition,Keywords.tag,Keywords.project_id FROM Keywords JOIN Users JOIN Projects ON Projects.project_id = Keywords.project_id AND Users.user_id = Keywords.user_id WHERE Users.user_id = %s AND Projects.project_id = %s;',(str(user_id),thwart(project_id),))
                keyword_set = c.fetchall()
                return render_template('paid-tools/rank-tracker-ultimate.html',keyword_set = keyword_set)
        else:
            flash("You must be logged in to use this tool")
            return redirect(url_for('sign_in'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('sign_in'))

# Rank tracker - add project
@app.route('/seo-tools/ultimate-rank-tracker/add-project',methods=["GET","POST"])
def rank_tracker_add_project():
    try:
        user_id = session['user_id'] 
        if session.get('logged_in') == True:
            if request.method == "POST":
                project = request.form['project']
                domain = request.form['domain']
                keyword_data_raw = request.form['keyword_data']
                keyword_data_raw = keyword_data_raw.strip()
                sql_project = add_project(keyword_data_raw,project,domain,user_id) # this is a list of sql statements
                flash(sql_project)
                return redirect(url_for('rank_tracker_ultimate'))
            else:
                return render_template('paid-tools/rank-tracker-add.html')
        else:
            flash("You must be logged in to use this tool")
            return redirect(url_for('sign_in'))
    except Exception as e:
        flash("You must be logged in to use this tool",e)
        return redirect(url_for('sign_in'))

# Rank tracker - delete project
@app.route('/seo-tools/ultimate-rank-tracker/delete-project',methods=["GET","POST"])
def rank_tracker_delete_project():
    try:
        user_id = session['user_id']    
        if session.get('logged_in') == True:
            c, conn = connection()
            try:
                projects = c.execute('SELECT DISTINCT Projects.project_id,Projects.client_name,Projects.domain FROM Projects JOIN Keywords JOIN Users ON Projects.project_id = Keywords.project_id AND Users.user_id = Keywords.user_id WHERE Keywords.user_id = %s;',(str(user_id),))
                if int(projects) > 0:
                    data = c.fetchall()
                    return render_template('paid-tools/rank-tracker-delete.html', data = data)
                else:
                    return render_template('paid-tools/rank-tracker-delete.html')
            except Exception as e:
                flash(e)    
                return render_template('paid-tools/rank-tracker-delete.html')
        else:
            flash("You must be logged in to use this tool")
            return redirect(url_for('sign_in'))
    except Exception as e:
        flash("You must be logged in to use this tool",e)
        return redirect(url_for('sign_in'))

# Rank tracker - delete project
@app.route('/seo-tools/ultimate-rank-tracker/confirm-delete',methods=["GET","POST"])
def confirm_delete():
        try:
            user_id = session['user_id']
            c, conn = connection()
            if session.get('logged_in') == True:
                if request.method == "GET":   
                    get_project_id = request.args.get('project_id')
                    c.execute("SELECT * FROM Projects WHERE project_id = %s;",(thwart(get_project_id),))
                    data = c.fetchone()
                    project_id= data[0]
                    client_name= data[1]
                    return render_template('paid-tools/rank-tracker-delete-confirm.html',project_id = project_id,client_name = client_name)
                if request.method == "POST":
                   project_id = request.form['project_id']
                   c.execute('SELECT key_id FROM Keywords WHERE project_id = %s;',(thwart(project_id),))
                   associated_keywords = c.fetchall()
                   flash(associated_keywords)
                   for keywords in associated_keywords:
                       c.execute("DELETE FROM Rankings WHERE key_id = %s;",(thwart(str(keywords[0])),))
                   c.execute("DELETE FROM Keywords WHERE project_id = %s;",(thwart(project_id),))
                   c.execute("DELETE FROM Projects WHERE project_id = %s;",(thwart(project_id),))
                   projects = c.execute('SELECT DISTINCT Projects.project_id,Projects.client_name,Projects.domain FROM Projects JOIN Keywords JOIN Users ON Projects.project_id = Keywords.project_id AND Users.user_id = Keywords.user_id WHERE Keywords.user_id = %s;',(str(user_id),))
                   data = c.fetchall()
                   session['projects'] = data
                   #flash('project deleted')
                   conn.commit()
                   c.close()
                   conn.close()
                   gc.collect()
                   return redirect(url_for('rank_tracker_delete_project'))
            else:
                flash("You must be logged in to use this tool")
                return redirect(url_for('sign_in'))
        except Exception as e:
            flash(e)    
            return render_template('paid-tools/rank-tracker-delete-confirm.html')    

# Rank tracker - edit keywords
@app.route('/seo-tools/ultimate-rank-tracker/edit',methods=["GET","POST"])
def edit_keywords():
    try:
        c, conn = connection()
        user_id = session['user_id']
        if session.get('logged_in') == True:
            if request.method == "GET":
                key_id = request.args.get('key_id')
                c.execute('SELECT * FROM Keywords WHERE key_id = %s AND user_id = %s;',(thwart(key_id),user_id,))
                data = c.fetchone()
                flash(data)
                return render_template('paid-tools/rank-tracker-edit-keywords.html',data = data)
            if request.method == "POST":
                keyword = request.form['keyword']
                search_volume = request.form['search_volume']
                competition = request.form['competition']
                tag = request.form['tag']
                key_id = request.form['key_id']
                c.execute('UPDATE Keywords SET keyword = %s, search_volume = %s, competition = %s, tag = %s WHERE key_id = %s AND user_id = %s;',(thwart(keyword),thwart(search_volume),thwart(competition),thwart(tag),thwart(key_id),user_id,))
                flash('Keyword edited')
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                return redirect(url_for('rank_tracker_ultimate'))
            else:
                return render_template('paid-tools/rank-tracker-edit-keywords.html')
        else:
            flash("You must be logged in to use this tool")
            return redirect(url_for('sign_in'))
    except Exception as e:
        flash(e)
        return render_template('paid-tools/rank-tracker-edit-keywords.html')

# Rank tracker - delete keywords
@app.route('/seo-tools/ultimate-rank-tracker/delete',methods=["GET","POST"])
def delete_keywords():
    try:
        c, conn = connection()
        user_id = session['user_id']
        if session.get('logged_in') == True:
            if request.method == "GET":
                key_id = request.args.get('key_id')
                c.execute('SELECT * FROM Keywords WHERE key_id = %s AND user_id = %s;',(thwart(key_id),user_id,))
                data = c.fetchone()
                flash(data)
                return render_template('paid-tools/rank-tracker-delete-keywords.html',data = data)
            if request.method == "POST":
                key_id = request.form['key_id']
                c.execute('DELETE FROM Rankings WHERE key_id = %s;',(thwart(key_id),))
                c.execute('DELETE FROM Keywords WHERE key_id = %s AND user_id = %s;',(thwart(key_id),user_id,))
                flash('Keyword deleted')
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                return redirect(url_for('rank_tracker_ultimate'))
                    
            else:
                return render_template('paid-tools/rank-tracker-delete-keywords.html')
        else:
            flash("You must be logged in to use this tool")
            return redirect(url_for('sign_in'))
    except Exception as e:
        flash(e)
        return render_template('paid-tools/rank-tracker-delete-keywords.html')

# Rank tracker - View rankings related to working project
@app.route('/seo-tools/ultimate-rank-tracker/rankings',methods=["GET","POST"])
def view_keyword_rankings():
        try:
            if session.get('logged_in') == True:
                c, conn = connection()
                user_id = session['user_id']
                project_id = session['working']
                if request.method == "POST":
                    start_date = request.form['start']
                    end_date = request.form['end']
                    c.execute('SELECT Keywords.keyword,Rankings.position,Rankings.est_traffic,urls.url_text,Keywords.search_volume,Rankings.timestmp FROM Users JOIN Projects JOIN Keywords JOIN Rankings JOIN urls ON Users.user_id = Keywords.user_id AND Projects.project_id = Keywords.project_id AND Keywords.key_id = Rankings.key_id AND Rankings.url_id = urls.url_id WHERE Keywords.user_id = %s AND Keywords.project_id = %s AND urls.url_text LIKE CONCAT(Projects.domain,"%%") AND Rankings.timestmp BETWEEN %s AND %s ORDER BY Rankings.timestmp ASC;',(thwart(str(user_id)),thwart(str(project_id)),thwart(start_date),thwart(end_date),))
                    rankings = c.fetchall()
                    return render_template('paid-tools/rank-tracker-rankings.html',rankings = rankings)
                else:
                    c.execute('SELECT Keywords.keyword,Rankings.position,Rankings.est_traffic,urls.url_text,Keywords.search_volume,Rankings.timestmp FROM Users JOIN Projects JOIN Keywords JOIN Rankings JOIN urls ON Users.user_id = Keywords.user_id AND Projects.project_id = Keywords.project_id AND Keywords.key_id = Rankings.key_id AND Rankings.url_id = urls.url_id WHERE Keywords.user_id = %s AND Keywords.project_id = %s AND urls.url_text LIKE CONCAT(Projects.domain,"%%") ORDER BY Rankings.timestmp ASC;',(thwart(str(user_id)),thwart(str(project_id)),))
                    rankings = c.fetchall()
                    return render_template('paid-tools/rank-tracker-rankings.html',rankings = rankings)
            else:
                flash("You must be logged in to use this tool")
                return redirect(url_for('sign_in'))
        except Exception as e:
            flash(e)
            return render_template('paid-tools/rank-tracker-rankings.html')

# Rank tracker - View all rankings
@app.route('/seo-tools/ultimate-rank-tracker/rankings-all',methods=["GET","POST"])
def view_keyword_rankings_all():
        try:
            if session.get('logged_in') == True:
                c, conn = connection()
                user_id = session['user_id']
                project_id = session['working']
                if request.method == "POST":
                    start_date = request.form['start']
                    end_date = request.form['end']
                    c.execute('SELECT Keywords.keyword,Rankings.position,Rankings.est_traffic,urls.url_text,Keywords.search_volume,Rankings.timestmp FROM Users JOIN Projects JOIN Keywords JOIN Rankings JOIN urls ON Users.user_id = Keywords.user_id AND Projects.project_id = Keywords.project_id AND Keywords.key_id = Rankings.key_id AND Rankings.url_id = urls.url_id WHERE Keywords.user_id = %s AND Keywords.project_id = %s AND Rankings.timestmp BETWEEN %s AND %s ORDER BY Rankings.timestmp ASC;',(thwart(str(user_id)),thwart(str(project_id)),thwart(start_date),thwart(end_date),))
                    rankings = c.fetchall()
                    return render_template('paid-tools/rank-tracker-rankings-all.html',rankings = rankings)

                else:
                    c.execute('SELECT Keywords.keyword,Rankings.position,Rankings.est_traffic,urls.url_text,Keywords.search_volume,Rankings.timestmp FROM Users JOIN Projects JOIN Keywords JOIN Rankings JOIN urls ON Users.user_id = Keywords.user_id AND Projects.project_id = Keywords.project_id AND Keywords.key_id = Rankings.key_id AND Rankings.url_id = urls.url_id WHERE Keywords.user_id = %s AND Keywords.project_id = %s ORDER BY Rankings.timestmp ASC;',(thwart(str(user_id)),thwart(str(project_id)),))
                    rankings = c.fetchall()
                    return render_template('paid-tools/rank-tracker-rankings-all.html', rankings = rankings)
            else:
                flash("You must be logged in to use this tool")
                return redirect(url_for('sign_in'))
        except Exception as e:
            flash(e)
            return render_template('paid-tools/rank-tracker-rankings-all.html')



if __name__ == "__main__":
    app.run()
