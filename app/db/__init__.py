from mongoengine import *
import time

import os

if not os.environ.get('DOCKER'):
    connect(host="localhost:27017")
else:
    connect(host="db:27017")

#Slower

# connect(username="andrew", password="sfhacks18", host="mongodb://main-shard-00-00-w6sow.mongodb.net:27017,main-shard-00-01-w6sow.mongodb.net:27017,main-shard-00-02-w6sow.mongodb.net:27017/test?ssl=true&replicaSet=main-shard-0&authSource=admin")

#Schemas

class Meet(Document):
    name = StringField()

    @staticmethod
    def all():
        return Meet.objects.order_by("name")

    @staticmethod
    def add(name):
        Meet(name = name).save()


class Player(Document):
    name = StringField(max_length=50)

class Time(Document):
    stroke = StringField()
    distance = IntField()
    time = FloatField()
    player = ReferenceField(Player)
    meet = ReferenceField(Meet)

# Roster
def getRoster():
    return Player.objects.order_by("name")

#Players

def addPlayer(name):
    Player(name=name).save()

def getPlayer(name):
    return Player.objects(name = name)[0]

def getPlayerById(id):
    return Player.objects.get(id=id)

def deletePlayer(name):
    p = Player.objects.get(name=name)
    times = Time.objects(player=p)
    for time in times:
        time.delete()
    p.delete()

def getTopPlayers(stroke, distance):
    players = []
    times = []

    for _ in range(5):
        query = Time.objects(stroke=stroke, distance=distance, player__nin=players).limit(1).order_by("time")
        if len(query) > 0:
            time = query[0]
            times.append(time)
            players.append(time.player)
    return times

# Times

def addTime(stroke, distance, time, player_id):
    Time(stroke=stroke, distance=distance, time=time, player=player_id).save()

def getAllTimesForPlayer(stroke, distance, player_id):
        return Time.objects(stroke=stroke, distance=distance, player=player_id).order_by("-id")
