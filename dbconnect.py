import MySQLdb
from MySQLdb import escape_string as thwart

def connection():
    conn = MySQLdb.connect(host="localhost", user="root",password="INPUT PASSWORD",db="Application")
    c = conn.cursor()
    return c,conn


def add_project(data,project,domain,user_id):
    c, conn = connection()
    try:
        # check if project and domain exists in projects table
        x = c.execute("SELECT * FROM Projects WHERE client_name = %s AND domain = %s;",(thwart(project),thwart(domain),))
        if int(x) > 0:
            c.execute("SELECT * FROM Projects WHERE client_name = %s AND domain = %s;",(thwart(project),thwart(domain),))
            get_project_id = c.fetchone()
            project_id = get_project_id[0]
            split_data = data.split('\n') # this is now a list
            for line in split_data:
                line = line.split(';')
                keyword = line[0]
                sv = line[1]
                competition = line[2]
                tag = line[3]
                c.execute("INSERT INTO Keywords(keyword,search_volume,competition,tag, project_id, user_id) VALUES (%s,%s,%s,%s,%s,%s);",(thwart(keyword),thwart(sv),thwart(competition),thwart(tag),project_id,user_id))
            conn.commit()
            c.close()
            conn.close()
            return "keywords added to existing project",project_id
        else:
            # create new project and insert associated keywords into database
            c.execute("INSERT INTO Projects(client_name,domain) VALUES (%s,%s);",(thwart(project),thwart(domain)))
            c.execute("SELECT * FROM Projects WHERE client_name = %s AND domain = %s;",(thwart(project),thwart(domain),))
            get_project_id = c.fetchone()
            project_id = get_project_id[0]
            split_data = data.split('\n') # this is now a list
            for line in split_data:
                line = line.split(';')
                keyword = line[0]
                sv = line[1]
                competition = line[2]
                tag = line[3]
                c.execute("INSERT INTO Keywords(keyword,search_volume,competition,tag, project_id, user_id) VALUES (%s,%s,%s,%s,%s,%s);",(thwart(keyword),thwart(sv),thwart(competition),thwart(tag),project_id,user_id))
            conn.commit()
            c.close()
            conn.close()
            return "project added",user_id

    except Exception as e:
        return e,project,domain, 
    
