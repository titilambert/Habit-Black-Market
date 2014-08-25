import requests

from flask import flash

import pyhabitmongo

from habitadmin import app

#app.config.get('HABIT_URL')


def set_headers(uuid, apitoken):
    headers = {"x-api-key": apitoken,
               "x-api-user": uuid,
               "Content-Type": "application/json;charset=UTF-8",
               }
    return headers


def login(uuid, apitoken):
    return get_user(uuid, apitoken) is not None

def get_user(uuid, apitoken):
    headers = set_headers(uuid, apitoken)
    res = requests.get(app.config.get('HABIT_URL') + "/api/v2/user", headers=headers, verify=False)
    data = res.json()
    if data.get('err', '') != '':
        flash('Error during login', 'danger')
        return None
    if data.get('id', '') == uuid:
        return data
    flash('Error during login', 'danger')
    return None

def buy_gems(uuid, apitoken, nb_gem):
    data = get_user(uuid, apitoken)
    if not 'stats' in data:
        return None
    if not 'gp' in data['stats']:
        return None
    current_gold = data['stats']['gp']
    if 20 * nb_gem > current_gold:
        # You need more gold
        flash('You need more gold', 'danger')
        return False
    pyhabitmongo.user_gold_to_gem(uuid, nb_gem)
    return True

def sell_gems(uuid, apitoken, nb_gem):
    data = get_user(uuid, apitoken)
    if not 'balance' in data:
        return None
    current_balance = data['balance']
    current_gems = current_balance * 4
    if current_gems < nb_gem:
        # You need more gems
        flash('You need more gems', 'danger')
        return False
    pyhabitmongo.user_gem_to_gold(uuid, nb_gem)
    return True

def transfer_gold(uuid, apitoken, receiver_uuid, gold):
    data = get_user(uuid, apitoken)
    if not 'stats' in data:
        return None
    if not 'gp' in data['stats']:
        return None
    current_gold = data['stats']['gp']
    if current_gold < gold:
        # You need more gold
        flash('You need more gold', 'danger')
        return False
    pyhabitmongo.user_transfer_gold(uuid, receiver_uuid, gold)
    return True


