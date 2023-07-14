# Date: 7/14/2023
# Mark Marrero

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import db_credentials as db_credentials
from datetime import datetime


app = Flask(__name__)
# db credentials
app.config["MYSQL_HOST"] = db_credentials.local_host
app.config["MYSQL_USER"] = db_credentials.local_user
app.config["MYSQL_PASSWORD"] = db_credentials.local_password
app.config["MYSQL_DB"] = db_credentials.local_db
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


mysql = MySQL(app)


# Routes
# homepage routes to index.html
@app.route('/')
def root():
    return render_template('index.html')

# games routes to games page
@app.route('/games', methods=["POST", "GET"])
def games():
    if request.method == "GET":
        read_query = 'select * from Games;'
        # cursor is the object linking the database and flask, sort of in lieu of
        # directly typing the commands into mysql
        cursor = mysql.connection.cursor()
        cursor.execute(read_query)
        # The cursor.fetchall() returns all results from the query.
        results = cursor.fetchall()
        return render_template("Games.j2", Games=results)

    if request.method == "POST":
        if request.form.get("addGame"):
            name = request.form['name']
            description = request.form['description']
            genre = request.form['genre']
            playtime = request.form['playtime']
            reqs = request.form['reqs']
            # set query to insert sql from DML
            query = 'INSERT INTO Games (name, description, genre, playtimeInMinutes, requirement) VALUES (%s, %s, %s, %s, %s);'
            cursor = mysql.connection.cursor()                
            cursor.execute(query, (name, description, genre, playtime, reqs))
            mysql.connection.commit()
            return redirect("/games")
        if request.form.get("editGame"):
            gameid = request.form["gameid"]
            name = request.form["name"]
            description = request.form["description"]
            genre = request.form["genre"]
            playtime = request.form["playtime"]
            reqs = request.form["reqs"]

            if name == "" and description == "" and genre == "" and playtime == "":
                query = "UPDATE Games SET requirement=%s WHERE gameid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (reqs, gameid))
                mysql.connection.commit()
                return redirect("/games")
            elif name == "" and description == "" and genre == "" and reqs == "":
                query = "UPDATE Games SET playtimeInMinutes=%s WHERE gameid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (playtime, gameid))
                mysql.connection.commit()
                return redirect("/games")
            elif name == "" and description == "" and playtime == "" and reqs == "":
                query = "UPDATE Games SET genre=%s WHERE gameid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (genre, gameid))
                mysql.connection.commit()
                return redirect("/games")
            elif name == "" and genre == "" and playtime == "" and reqs == "":
                query = "UPDATE Games SET description=%s WHERE gameid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (description, gameid))
                mysql.connection.commit()
                return redirect("/games")
            elif description == "" and genre == "" and playtime == "" and reqs == "":
                query = "UPDATE Games SET name=%s WHERE gameid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (name, gameid))
                mysql.connection.commit()
                return redirect("/games")
            else:
                query = "UPDATE Games SET name=%s, description=%s, genre=%s, playtimeInMinutes=%s, requirement=%s WHERE gameid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query,(name, description, genre, playtime, reqs, gameid))
                mysql.connection.commit()
                return redirect("/games")

        if request.form.get("search_Game"):
            gameName = request.form.get("gameSearch")
            cursor = mysql.connection.cursor()
            cursor.execute( "SELECT gameid, name, description, genre, playtimeInMinutes, requirement from Games WHERE name LIKE %s",(f"%{gameName}%",))
            mysql.connection.commit()
            data = cursor.fetchall()
            return render_template('Game_Search.j2', data=data)
    
@app.route("/delete_Game/<int:gameid>")
def delete_game(gameid):
    query = "delete from Games where gameid= %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (gameid,))
    mysql.connection.commit()
    return redirect("/games")

# players routes to player page and player search page 
@app.route('/players', methods=["POST", "GET"])
def players():
    if request.method == "GET":
        read_query = 'select * from Players;'
        # cursor is the object linking the database and flask, in lieu of
        # directly typing the commands into mysql
        cursor = mysql.connection.cursor()
        cursor.execute(read_query)
        # The cursor.fetchall() returns all results from the query.
        results = cursor.fetchall()   
        return render_template("Players.j2", Players=results)
    
    if request.method == "POST":
        if request.form.get("addPlayer"):
            name = request.form["fname"]
            phone = request.form["phone"]
            email = request.form["email"]
            # set query to insert sql from DML
            query = 'INSERT INTO Players (name, phone, email) VALUES (%s, %s, %s);'
            cursor = mysql.connection.cursor()                
            cursor.execute(query, (name, phone, email))
            mysql.connection.commit()
            return redirect("/players")
        
        if request.form.get("editPlayer"):
            playerid = request.form['playerid']
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            if phone == "" and email == "":
                query = "UPDATE Players SET name=%s WHERE playerid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (name, playerid))
                mysql.connection.commit()
            elif phone == "" and name == "":
                query = "UPDATE Players SET email=%s WHERE playerid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (email, playerid))
                mysql.connection.commit()
            elif phone == "":
                query = "UPDATE Players SET name=%s, email=%s WHERE playerid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (name,email, playerid))
                mysql.connection.commit()
            elif email == "" and name == "":
                query = "UPDATE Players SET phone=%s WHERE playerid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (phone, playerid))
                mysql.connection.commit()
            elif email == "":
                query = "UPDATE Players SET name=%s, phone=%s WHERE playerid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (name, phone, playerid))
                mysql.connection.commit()

            else:
                query = 'UPDATE Players SET name=%s, phone=%s, email=%s WHERE playerid=%s'
                cursor = mysql.connection.cursor()                
                cursor.execute(query, (name, phone, email, playerid))
                mysql.connection.commit()
            return redirect("/players")
       
        if request.form.get("search_Player"):
            playerName = request.form.get("playerSearch")
            cursor = mysql.connection.cursor()
            cursor.execute( "SELECT playerid,name,phone,email from Players WHERE name LIKE %s",(f"%{playerName}%",))
            mysql.connection.commit()
            data = cursor.fetchall()
            return render_template('Player_Search.j2', data=data)
         
@app.route("/delete_Player/<int:playerid>")
def delete_Player(playerid):
    query = "delete from Players where playerid= %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (playerid,))
    mysql.connection.commit()
    return redirect("/players")
    
# groups routes to groups page and groups search page    
@app.route('/groups', methods=["POST", "GET"])
def groups():
    if request.method == "GET":
        read_query = 'select * from GamerGroups;'
        # cursor is the object linking the database and flask, in lieu of
        # directly typing the commands into mysql
        cursor = mysql.connection.cursor()
        cursor.execute(read_query)
        # The cursor.fetchall() returns all results from the query.
        results = cursor.fetchall()
        return render_template("GamerGroups.j2", GamerGroups=results)

    if request.method == "POST":
        if request.form.get("addGroup"):
            name = request.form['name']
            meetdays = request.form['meetdays']
            # set query to insert sql from DML
            query = 'INSERT INTO GamerGroups (groupname, meetday) VALUES (%s, %s);'
            cursor = mysql.connection.cursor()                
            cursor.execute(query, (name, meetdays))
            mysql.connection.commit()
            return redirect("/groups")
        if request.form.get("editGroup"):
            groupid = request.form["groupid"]
            name = request.form["name"]
            meetdays = request.form["meetdays"]
            if name == "":
                query = "UPDATE GamerGroups SET meetday=%s WHERE groupid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (meetdays, groupid))
                mysql.connection.commit()
                return redirect("/groups")
            elif meetdays == "":
                query = "UPDATE GamerGroups SET groupname=%s WHERE groupid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query, (name, groupid))
                mysql.connection.commit()
                return redirect("/groups")  
            else:
                query = "UPDATE GamerGroups SET groupname=%s, meetday=%s WHERE groupid=%s"
                cursor = mysql.connection.cursor()
                cursor.execute(query,(name, meetdays, groupid))
                mysql.connection.commit()
                return redirect("/groups")
        if request.form.get("search_Group"):
            groupName = request.form.get("groupSearch")
            cursor = mysql.connection.cursor()
            cursor.execute( "SELECT groupid, groupname, meetday from GamerGroups WHERE groupname LIKE %s",(f"%{groupName}%",))
            mysql.connection.commit()
            data = cursor.fetchall()
            return render_template('Group_Search.j2', data=data)
    
@app.route("/delete_Group/<int:groupid>")
def delete_group(groupid):
    query = "delete from GamerGroups where groupid= %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (groupid,))
    mysql.connection.commit()
    return redirect("/groups")

# group games route to groupgames page
@app.route("/groupgames", methods=["POST", "GET"])
def groupgames():
    if request.method == "GET":
        read_query = '''SELECT groupgamesid, GamerGroups.groupid, Games.gameid FROM GroupGames
        INNER JOIN GamerGroups ON GamerGroups.groupid=GroupGames.groupid
        INNER JOIN Games ON Games.gameid=GroupGames.gameid;'''
        # cursor is the object linking the database and flask, in lieu of
        # directly typing the commands into mysql
        cursor = mysql.connection.cursor()
        cursor.execute(read_query)
        # The cursor.fetchall() returns all results from the query.
        results = cursor.fetchall()
        read_query2 = 'SELECT groupid, groupname from GamerGroups'
        cursor = mysql.connection.cursor()
        cursor.execute(read_query2)
        group_id_data = cursor.fetchall()
        read_query3 = 'SELECT gameid, name from Games'
        cursor = mysql.connection.cursor()
        cursor.execute(read_query3)
        game_id_data = cursor.fetchall()
        return render_template("GroupGames.j2", GroupGames=results, GamerGroups = group_id_data, Games = game_id_data)
    if request.method == "POST":
        if request.form.get("add_GroupGame"):
            groupid = request.form['groupid']
            gameid = request.form['gameid']
            query = 'INSERT INTO GroupGames (groupid, gameid) VALUES (%s, %s);'
            cursor = mysql.connection.cursor()
            cursor.execute(query, (groupid, gameid))
            mysql.connection.commit()
            return redirect("/groupgames")
        if request.form.get("editGroupGame"):
            groupgameid = request.form.get("groupgameid")
            groupid = request.form['groupid']
            gameid = request.form['gameid']
            if groupid == "":
                query = 'UPDATE GroupGames SET gameid=%s WHERE groupgameid=%s;'
                cursor = mysql.connection.cursor()
                cursor.execute(query, (gameid, groupgameid))
                mysql.connection.commit()
                return redirect("/groupgames")
            elif gameid == "":
                query = 'UPDATE GroupGames SET groupid=%s WHERE groupgamesid=%s;'
                cursor = mysql.connection.cursor()
                cursor.execute(query, (groupid, groupgameid))
                mysql.connection.commit()
                return redirect("/groupgames")
            else:
                query = 'UPDATE GroupGames SET groupid=%s, gameid=%s WHERE groupgamesid=%s;'
                cursor = mysql.connection.cursor()
                cursor.execute(query, (groupid, gameid, groupgameid))
                mysql.connection.commit()
                return redirect("/groupgames")

# group membership routes to group membership page
@app.route("/groupmembership", methods=["POST", "GET"])
def groupmembership():
    if request.method == "GET":
        read_query = '''SELECT groupmembershipid, GamerGroups.groupid, Players.playerid, datejoin, currentplayer FROM GroupMemberships
            INNER JOIN GamerGroups ON GamerGroups.groupid=GroupMemberships.groupid
            INNER JOIN Players ON Players.playerid=GroupMemberships.playerid;'''
        cursor = mysql.connection.cursor()
        cursor.execute(read_query)
        # The cursor.fetchall() returns all results from the query.
        results = cursor.fetchall()
        read_query2 = 'SELECT groupid, groupname from GamerGroups'
        cursor = mysql.connection.cursor()
        cursor.execute(read_query2)
        group_id_data = cursor.fetchall()
        read_query3 = 'SELECT playerid, name from Players'
        cursor = mysql.connection.cursor()
        cursor.execute(read_query3)
        player_id_data = cursor.fetchall()
        return render_template("Group_Membership.j2", GroupMemberships=results, GamerGroups = group_id_data, Players = player_id_data)
    if request.method == "POST":
        if request.form.get("add_GroupMembership"):
            groupid = request.form['groupid']
            playerid = request.form['playerid']
            datejoin = request.form['datejoin']
            currentplayer = request.form['currentplayer']
            query = 'INSERT INTO GroupMemberships (groupid, playerid, datejoin, currentplayer) VALUES (%s, %s,%s,%s);'
            cursor = mysql.connection.cursor()
            cursor.execute(query, (groupid, playerid, datejoin, currentplayer))
            mysql.connection.commit()
            return redirect("/groupmembership")    
        if request.form.get("editGroupMembership"):
            groupmembershipid = request.form.get("groupmembershipid")
            groupid = request.form['groupid']
            playerid = request.form['playerid']
            datejoin = request.form['datejoin']
            currentplayer = request.form['currentplayer']
            if datejoin == "" or datejoin == None:
                query = 'UPDATE GroupMemberships SET groupid=%s, playerid=%s, currentplayer=%s WHERE groupmembershipid=%s;'
                cursor = mysql.connection.cursor()
                cursor.execute(query, (groupid, playerid, currentplayer, groupmembershipid))
                mysql.connection.commit()
                return redirect("/groupmembership")
            else:
                query = 'UPDATE GroupMemberships SET groupid=%s, playerid=%s, datejoin=%s, currentplayer=%s WHERE groupmembershipid=%s;'
                cursor = mysql.connection.cursor()
                cursor.execute(query, (groupid, playerid, datejoin, currentplayer, groupmembershipid))
                mysql.connection.commit()
                return redirect("/groupmembership")

# List to store events
events = []

# Route to display the calendar
@app.route('/events')
def calendar():
    return render_template('Events.j2', events=events)

# Route to create a new event
@app.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        events.append({'id': len(events) + 1, 'title': title, 'date': date})
        return redirect('/events')
    return render_template('Create_Event.j2')

# Route to edit an existing event
@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    event = events[event_id - 1]
    if request.method == 'POST':
        event['title'] = request.form['title']
        event['date'] = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        return redirect('/events')
    return render_template('Edit_Event.j2', event=event)

# Route to delete an existing event
@app.route('/events/<int:event_id>/delete')
def delete_event(event_id):
    events.pop(event_id - 1)
    return redirect('/events')


# Listener
if __name__ == "__main__":

    #Start the app on port 10255, it will be different once hosted
    app.run(port=10255, debug=True)
