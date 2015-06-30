#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print "Failed to connect to the database"


def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    query = "TRUNCATE matches CASCADE;"
    c.execute(query)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    query = "TRUNCATE players CASCADE;"
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
    query = "SELECT COUNT(id) FROM players;"
    c.execute(query)
    num = c.fetchall()
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
    c.execute(query, param)
    conn.commit()
    conn.close()


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
    query = "SELECT id,name,wins,matches FROM Standings ORDER BY wins DESC;"
    c.execute(query)
    results = c.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = connect()
    query1 = "INSERT INTO Matches (player, opponent, result) values (%s, %s, 1)"
    param1 = (winner, loser)
    c.execute(query1, param1)
    query2 = "INSERT INTO Matches (player, opponent, result) values (%s, %s, 0)"
    param2 = (loser, winner)
    c.execute(query2, param2)
    conn.commit()
    conn.close()


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
    conn, c = connect()
    query = "SELECT id,name,wins FROM Standings ORDER BY Wins DESC;"
    c.execute(query)
    results = c.fetchall()
    conn.close()
    i = 0
    pairings = []
    playerAids = []
    playerAnames = []
    playerBids = []
    playerBnames = []
    while i < len(results):
        playerAids.append(results[i][0])
        playerAnames.append(results[i][1])
        playerBids.append(results[i + 1][0])
        playerBnames.append(results[i + 1][1])
        i += 2
    pairings = zip(playerAids, playerAnames, playerBids, playerBnames)
    return pairings
