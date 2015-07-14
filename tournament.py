#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class DB:
    def __init__(self, db_con_str="dbname=tournament"):
        """
        Create a database connection with the connection string
        :param str db_con_str: Contains the database connection string, with a default value
        when no argument is passed to the parameter
        """
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """
        return the current cursor of the database
        """
        return self.conn.cursor()

    def execute(self, sql_query_string, param=None, and_close=False):
        """
        Executes SQL queries
        :param str sql_query_string: contain the query string to be executed
        :param bool and_close, if true, closes the database connection after executing
        and committing the SQL Query
        """
        cursor = self.cursor()
        if param:
            cursor.execute(sql_query_string, param)
        else:
            cursor.execute(sql_query_string)
        if and_close:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not and_close else None}

    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        #use DB class to get database connection and cursor
        db = DB()
        cursor = db.cursor()
        return db.conn, cursor
    except:
        print "Failed to connect to the database"


def deleteMatches():
    """Remove all the match records from the database."""
    #TRUNCATE is faster than DELETE
    #But it bypasses the transaction log and cannot be restored
    query = "TRUNCATE matches CASCADE;"
    DB().execute(query, None, True)

def deletePlayers():
    """Remove all the player records from the database."""
    query = "TRUNCATE players CASCADE;"
    DB().execute(query, None, True)

def countPlayers():
    """Returns the number of players currently registered."""
    #Count number of different ids => number of players
    query = "SELECT COUNT(id) FROM players;"
    transaction = DB().execute(query)
    num = transaction["cursor"].fetchall()
    transaction["conn"].close()
    return num[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, c = connect()
    # safely insert, and use python tuple
    query = "INSERT INTO players (name) values (%s)"
    param = (name, )
    DB().execute(query, param, True)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = connect()
    #Get result from view Standings 
    query = "SELECT id,name,wins,matches FROM Standings ORDER BY wins DESC;"
    transaction = DB().execute(query)
    #didn't close the connection, fetch results
    results = transaction["cursor"].fetchall()
    transaction["conn"].close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    #Insert winner, loser into Matches table to record a match
    query = "INSERT INTO Matches (winner, loser) values (%s, %s)"
    param = (winner, loser)
    transaction = DB().execute(query, param, True)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    #Select pairs of players with the same wins from View Wins
    query = "SELECT a.id, a.name, b.id, b.name\
            FROM Wins as a JOIN Wins as b\
            ON a.n = b.n WHERE a.id > b.id\
            "
    transaction = DB().execute(query)
    results = transaction["cursor"].fetchall()
    transaction["conn"].close()
    return results
