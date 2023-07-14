create database if not exists gameappdb;

create table if not exists Players(
	playerid int auto_increment not null,
    name varchar(150) not null,
    phone varchar(15),
    email varchar(150),
    primary key (playerid)
);

INSERT INTO Players (
    name,
    phone,
    email
)
VALUES (
    'Alex Svoboda',
    '9077753455',
    'asvoboda@hello.com'
),
(
    'Ryan Patel',
    '5552345678',
    'ryan.patel@hello.com'
),
(
    'Emma Williams',
    '5552346789',
    'emWill@hello.com'
);

create table if not exists Games(
	gameid int auto_increment not null,
    name varchar(150) not null,
    description text(500) not null,
    genre varchar(150) not null,
    playtimeInMinutes int not null,
    requirement varchar(150) not null,
    primary key (gameid)
);

INSERT INTO Games (
    name,
    description,
    genre,
    playtimeInMinutes,
    requirement
)
VALUES (
    'Galactic Conquest',
    'Players take control of the galaxy',
    'Strategy',
    90,
    'Optional addon is avaliable to play'
),
(
    'Treasure Hunters',
    'Explore ancient ruins in the search of artifacts',
    'Adventure',
    60,
    'None'
),
(
    'Farm Life',
    'Enjoy a new life as a farmer by managing your farm and fighting for the highest profits',
    'Simulation/Strategy',
    40,
    'Additional crops expansion required'
);

create table if not exists GamerGroups (
	groupid int auto_increment not null,
    groupname varchar(150) not null,
    meetday varchar (150) not null,
    primary key (groupid)
);
INSERT INTO GamerGroups(
    groupname,
    meetday
)
VALUES (
    'Game on!',
    'Monday and Friday'
),
(
    'Without Boarders',
    'Every other Wednesday'
),
(
    'Roll and Play',
    'Friday and Sunday'
);

create table if not exists GroupGames (
	groupgamesid int auto_increment not null,
    groupid int,
    gameid int null,
    primary key (groupgamesid),
    foreign key (groupid) references GamerGroups (groupid)
    ON DELETE CASCADE,
    foreign key (gameid) references Games (gameid)
    ON DELETE CASCADE
);
INSERT INTO GroupGames (
    groupid,
    gameid
)
VALUES (
    (SELECT groupid FROM GamerGroups WHERE groupid = '1'),
    (SELECT gameid FROM Games WHERE gameid = '15')
),
(
    (SELECT groupid FROM GamerGroups WHERE groupid = '2'),
    (SELECT gameid FROM Games WHERE gameid = '21')
),
(
    (SELECT groupid FROM GamerGroups WHERE groupid = '3'),
    (SELECT gameid FROM Games WHERE gameid = '27')
);

create table if not exists GroupMemberships (
	groupmembershipid int auto_increment not null,
    groupid int,
    playerid int,
    datejoin date,
    currentplayer varchar(25),
    primary key (groupmembershipid),
    foreign key (groupid) references GamerGroups (groupid)
    ON DELETE CASCADE,
    foreign key (playerid) references Players (playerid)
    ON DELETE CASCADE
);
INSERT INTO GroupMemberships (
    groupid,
    playerid,
    datejoin,
    currentplayer
)
VALUES (
    1,
    2,
    '2022-05-15',
    'Yes'
),
(
    3,
    3,
    '2021-12-12',
    'Yes'
),
(
    2,
    1,
    '2018-07-07',
    'No'
);
