CREATE TABLE IF NOT EXISTS member
(id SERIAL NOT NULL PRIMARY KEY,
nickname VARCHAR(50) NOT NULL,
passcache VARCHAR(129) NOT NULL,
wins SMALLINT,
defeat SMALLINT,
draw SMALLINT,
drp SMALLINT NOT NULL,
maxDRP SMALLINT NOT NULL,
commandID SMALLINT);

CREATE TABLE IF NOT EXISTS session
(userID INTEGER NOT NULL,
sessionID VARCHAR(129) NOT NULL,
createData INTEGER NOT NULL,
endData INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS match
(matchID SERIAL NOT NULL PRIMARY KEY,
status SMALLINT NOT NULL,
firstPlayerID INTEGER NOT NULL,
secondPlayerID INTEGER NOT NULL,
firstDRP SMALLINT NOT NULL,
secondDRP SMALLINT NOT NULL,
firstRateChange SMALLINT,
secondRateChange SMALLINT,
commentary TEXT);

CREATE TABLE IF NOT EXISTS team
(teamID SERIAL NOT NULL PRIMARY KEY,
name VARCHAR(120),
top SMALLINT NOT NULL,
logo TEXT,
description TEXT,
color VARCHAR(20));