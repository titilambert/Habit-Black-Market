#!/usr/bin/python

from datetime import datetime
import uuid

from pymongo import MongoClient

client = MongoClient()

client = MongoClient('localhost', 27017)

habitrpg_db = client.habitrpg


def clear_db():
    import pdb;pdb.set_trace()
    client.drop_database("habitrpg")


def guild_add(name, description, leader, public=False):
    leader_id = user_get_id(leader)
    privacy == "private"
    if public == True:
        privacy == "public"
    if leader_id is None:
        return 
    guild = {
             "_id" : str(uuid.uuid4()),
             "balance" : 1,
             "challengeCount" : 0,
             "challenges": [],
             "chat" : [ ],
             "description": description,
             "invites" : [ ],
             "leader" : leader_id,
             "memberCount" : 1,
             "members" : [leader_id],
             "name" : name,
             "privacy" : privacy,
             "quest": {"progress": {"collect": {} },
                       "active" : false
                       },
             "type" : "guild" }
    habitrpg_db.groups.insert(guild)


def guild_get_id(guild):
    guild = habitrpg_db.groups.find_one({"name": guild,
                                         "type" : "guild"})
    return guild.get("_id", None)


def guild_user_add(guild, user):
    user_id = user_get_id(username)
    if user_id is None:
        return
    guild_id = guild_get_id(username)
    if guild_id is None:
        return
    # TODO: check the presence of this user before adding

    habitrpg_db.groups.update({"_id": guild_id},
                              {"$push": {"members": user_id}},
                              )
    # TODO: check members before increase memberCount
    habitrpg_db.groups.update({"_id": guild_id},
                              {"$inc": {"memberCount": 1}},
                              )


def guild_user_del(guild, user):
    pass


def challenge_get_id(challenge):
    challenge = habitrpg_db.challenge.find_one({"name": guild})
    return challenge.get("_id", None)


def challenge_add(name, description, guild, leader, tag, prize):
    leader_id = user_get_id(username)
    if leader_id is None:
        return
    guild_id = guild_get_id(username)
    if guild_id is None:
        return
    challenge = {"name": name,
                 "description": description,
                 "leader": leader_id,
                 "group": guild_id,
                 "shortName": tag,
                 "prize": int(prize),
                 "memberCount": 0,
                 "members": [leader_id],
                 "timestamp": datetime.now(),
                 "rewards": [],
                 "todos": [],
                 "dailys": [],
                 "habits": [],
                 "official": false,
                 "_id": str(uuid.uuid4()),
                 "__v": 0}
    habitrpg_db.challenge.insert(challenge)
    # TODO check the state of the last command
    habitrpg_db.groups.update({"_id": guild_id},
                              {"$inc": {"challengeCount": 1}},
                              )


def challenge_reward_add(challenge, name, notes, value, difficulty=1):
    challenge_id = challenge_get_id(challenge)
    if challenge_id is None:
        return
    
    habitrpg_db.groups.update({"_id": challenge_id},
                              {"$push": {"rewards": {"text": name,
                                                     "attribute": "str",
                                                     "priority": difficulty,
                                                     "value": int(value),
                                                     "notes": notes,
                                                     "dateCreated": datetime.now(),
                                                     "id": str(uuid.uuid4()),
                                                     "type": "reward"
                                                     }
                                         }
                               },
                              )


def challenge_todo_add(challenge, name, notes, due_date, difficulty=1):
    # difficulty
    # easy = 1
    # medium = 1.5
    # difficult = 2
    challenge_id = challenge_get_id(challenge)
    if challenge_id is None:
        return

    habitrpg_db.groups.update({"_id": challenge_id},
                              {"$push": {"todos": {"text": name,
                                                     "date" : due_date,
                                                     "attribute" : "str",
                                                     "priority" : difficulty,
                                                     "value" : 0,
                                                     "notes" : notes,
                                                     "dateCreated" : datetime.now(),
                                                     "id": str(uuid.uuid4()),
                                                     "checklist": [],
                                                     "collapseChecklist": False,
                                                     "completed": False,
                                                     "type": "todo",
                                                     },
                                         } 
                               },
                              ) 


def challenge_daily_add(challenge, name, notes, difficulty=1, repeat=("f", "th", "w", "t", "m")):
    challenge_id = challenge_get_id(challenge)
    if challenge_id is None:
        return

    days = {"m": False,
            "t": False,
            "w": False,
            "th": False,
            "f": False,
            "s": False,
            "su": False,
            }
    for day in days.keys():
        if day in repeat:
            days[day] = True

    habitrpg_db.groups.update({"_id": challenge_id},
                              {"$push": {"dailys": {"text": name,
                                                    "attribute": "str",
                                                    "priority": difficulty,
                                                    "value": 0,
                                                    "notes": notes,
                                                    "dateCreated": datetime.now(),
                                                    "id": str(uuid.uuid4()),
                                                    "streak": 0,
                                                    "checklist": [],
                                                    "collapseChecklist": False,
                                                    "repeat": {"su": days['su'],
                                                               "s": days['s'],
                                                               "f": days['f'],
                                                               "th": days['th'],
                                                               "w": days['w'],
                                                               "t": days['t'],
                                                               "m": days['m'],
                                                               },
                                                    "completed": False,
                                                    "history": [],
                                                    "type": "daily"
                                                    },
                                         }
                               }
                              )

def challenge_habit_add(challenge, name, notes, difficulty=1, up=True, down=False):
    challenge_id = challenge_get_id(challenge)
    if challenge_id is None:
        return

    habitrpg_db.groups.update({"_id": challenge_id},
                              {"$push": {"habits": {"text": name,
                                                    "attribute": "str",
                                                    "priority": difficulty,
                                                    "value": 0,
                                                    "notes": notes,
                                                    "dateCreated": datetime.now(),
                                                    "id": str(uuid.uuid4()),
                                                    "down": down,
                                                    "up": up,
                                                    "history": [ ],
                                                    "type": "habit",
                                                    },
                                         }
                               }
                              )

def user_get_id(username):
    user = habitrpg_db.users.find_one({"auth.local.username": username})
    return user.get("_id", None)

def user_set_contributor(username):
    user_id = user_get_id(username)
    if user_id is None:
        return
    habitrpg_db.users.update({"_id": user_id}, 
                             {"$set": {'contributor.admin': True}}
                             )

def user_set_subscription(username):
    user_id = user_get_id(username)
    if user_id is None:
        return
    habitrpg_db.users.update({"_id": user_id},
                             {"$set": {'purchased.plan': {"planId": 'basic_earned',
                                                          "customerId": str(uuid.uuid4()),
                                                          "dateUpdated": datetime.now(),
                                                          "gemsBought": 0, 
                                                          "mysteryItems": [ ],
                                                          "paymentMethod": 'Stripe',
                                                          "dateTerminated": None,
                                                          }
                                      }
                              }
                             )


def user_increase_balance(username, balance):
    user_id = user_get_id(username)
    if user_id is None:
        return
    habitrpg_db.users.update({"_id": user_id},
                             {"$set": {'balance': balance}}
                             )

def user_add(username, email):
    """ Create new user """
    # TODO
    # salt and password
    # Check if already exists
    user = {
            "_id": str(uuid.uuid4()),
            "apiToken": str(uuid.uuid4()),
            "achievements": {"beastMaster": False,
                              "challenges": [ ]
                              },
            "auth": {"timestamps": {"loggedin": datetime.now(),
                                    "created": datetime.now()
                                    },
                     "local": {"username": username,
                               "email": email,
                               "salt": "2794e8ce42",
                               "hashed_password": "b015185fbffcf7f72e98b0591728fff9c0a6efd2", # password is password
                               },
                     },
            "backer": {  },
            "balance": 0,
            "challenges": [ ],
            "contributor": {  },
            "dailys": [ ],
            "filters": {  },
            "flags": {"levelDrops": {  },
                      "freeRebirth": False,
                      "rebirthEnabled": False,
                      "classSelected": False,
                      "rewrite": True,
                      "newStuff": False,
                      "itemsEnabled": False, 
                      "dropsEnabled": False,
                      "showTour": True,
                      "customizationsNotification": False
                      },
            "habits": [ ],
            "history": {"todos": [ ],
                        "exp": [ ]
                        },
            "invitations": {"guilds": [ ]},
            "items": {"lastDrop": {"count": 0,
                                   "date": datetime.now(),
                                    },
                      "quests": {  },
                      "mounts": {  },
                      "food": {  },
                      "hatchingPotions": {  },
                      "eggs": {  },
                      "pets": {  },
                      "special": {"valentineReceived": [ ],
                                  "snowball": 0
                                  },
                      "gear": {"costume": {"shield": "shield_base_0",
                                           "head": "head_base_0",
                                           "armor": "armor_base_0",
                                           "weapon": "weapon_base_0"
                                           },
                               "equipped": {"shield": "shield_base_0",
                                            "head": "head_base_0",
                                            "armor": "armor_base_0",
                                            "weapon": "weapon_warrior_0"
                                            },
                               "owned": {"weapon_warrior_0": True}
                               },
                      },
            "lastCron": datetime.now(),
            "newMessages": {"undefined": {"value": False } },
            "party": {"quest": {"progress": {"collect": {  },
                                             "down": 0,
                                             "up": 0,
                                             },
                                },
                      "order": "level"
                     },
            "preferences": {"advancedCollapsed": False,
                            "allocationMode": "flat",
                            "dayStart": 0,
                            "disableClasses": False,
                            "hair": {"bangs": 0,
                                     "base": 0,
                                     "beard": 0,
                                     "color": "white",
                                     "flower": 0,
                                     "mustache": 0
                                     },
                            "hideHeader": False,
                            "language": "en",
                            "newTaskEdit": False,
                            "shirt": "black",
                            "size": "slim",
                            "skin": "ddc994",
                            "sleep": False,
                            "stickyHeader": True,
                            "tagsCollapsed": False,
                            "timezoneOffset": 240,
                            "toolbarCollapsed": False
                            },
            "profile": {"name": username.lower()},
            "purchased": {"plan": {"mysteryItems": [ ],
                                   "gemsBought": 0
                                   },
                          "txnCount": 0,
                          "background": {  },
                          "shirt": {  },
                          "hair": {  },
                          "skin": {  },
                          "ads": False
                          },
            "rewards": [ ],
            "stats": {"training": {"con": 0,
                                   "str": 0,
                                   "per": 0,
                                   "int": 0
                                   },
                      "buffs": {"snowball": False,
                                "streaks": False,
                                "stealth": 0,
                                "con": 0,
                                "per": 0,
                                "int": 0,
                                "str": 0
                                },
                      "per": 0,
                      "int": 0,
                      "con": 0,
                      "str": 0,
                      "points": 0,
                      "class": "warrior",
                      "lvl": 1,
                      "gp": 0,
                      "exp": 0,
                      "mp": 10,
                      "hp": 50
                      },
            "tags": [ ],
            "todos": [ ]
            }
    habitrpg_db.users.insert(user)
    


