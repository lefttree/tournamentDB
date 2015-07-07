-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop database if there is already a tournament database
DROP DATABASE IF EXISTS tournament;
-- Create and connect to database
CREATE DATABASE tournament;
\c tournament;

/*
* Players table 
* columns: id - player's id, name - player's name
* purpose: represent each player
*/
CREATE TABLE Players (
	id SERIAL primary key,
	name varchar(255)
);

/*
* Matches table
* columns: id - match's id, winner - winner's player id, loser - loser's player id
* purpose: represent each match's result
*/
CREATE TABLE Matches (
	id SERIAL primary key,
	winner int references players(id),
	loser int references players(id)
	);

/*
* Wins view
* column: players.id, n - player's wins
* purpose: count each player's number of wins
*/
CREATE VIEW Wins AS
	SELECT Players.id, COUNT(Matches.winner) AS n
	FROM Players
	LEFT JOIN Matches
	ON Players.id = Matches.winner
	GROUP BY Players.id;

/*
* Count view
* column: players.id, n - player's matches
* purpose: count each player's number of matches
*/
CREATE VIEW Count AS
	SELECT Players.id, COUNT(Matches.winner) AS n
	FROM Players
	LEFT JOIN Matches
	ON Players.id = Matches.winner OR Players.id = Matches.loser
	GROUP BY Players.id;

/*
* Wins view
* column: players.id, players.name, Wins.n, Count.n
* purpose: combine each player's number of wins and matches
*/
CREATE VIEW Standings AS
	SELECT Players.id, Players.name, Wins.n as wins,Count.n as matches
	FROM Players, Count, Wins
	WHERE Players.id = Wins.id and Wins.id = Count.id;

