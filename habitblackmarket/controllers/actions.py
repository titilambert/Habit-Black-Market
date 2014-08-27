# -*- coding: utf-8 -*-
import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from habitblackmarket.libs import pyhabitapi

from habitblackmarket import app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        if request.form.get('uuid', '') == '':
            flash('No UUID', 'danger')
            return redirect(url_for('publish'))
        if request.form.get('apitoken', '') == '':
            flash('No API token', 'danger')
            return redirect(url_for('publish'))
        if request.form.get('title', '') == '':
            flash('No title', 'danger')
            return redirect(url_for('publish'))
        if request.form.get('content', '') == '':
            flash('No content', 'danger')
            return redirect(url_for('publish'))

        uuid = request.form.get('uuid', '')
        apitoken = request.form.get('apitoken', '')
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        subtitle = request.form.get('subtitle', '')
        # TODO decorator
        if not pyhabitapi.login(uuid, apitoken):
            return redirect(url_for('publish'))
        ret = pyhabitapi.publish(uuid, apitoken, title, subtitle, content)
        if ret == True:
            flash('News published', 'success')
            return redirect(url_for('index'))
        elif ret is not False:
            flash('Unknown error', 'danger')

    return render_template('actions/publish.html',
                           habit_link=app.config['HABIT_LINK'])


@app.route('/gems/buy', methods=['GET', 'POST'])
def buy_gems():
    if request.method == 'POST':
        if request.form.get('uuid', '') == '':
            flash('No UUID', 'danger')
            return redirect(url_for('buy_gems'))
        if request.form.get('apitoken', '') == '':
            flash('No API token', 'danger')
            return redirect(url_for('buy_gems'))
        if request.form.get('gems') == '':
            flash('Bad gems input', 'danger')
            return redirect(url_for('buy_gems'))

        try:
            gems = int(request.form.get('gems', 0))
        except:
            flash('Bad gems input', 'danger')
            return redirect(url_for('buy_gems'))
        if gems < 1:
            flash('Bad gems input', 'danger')
            return redirect(url_for('buy_gems'))

        uuid = request.form.get('uuid', '')
        apitoken = request.form.get('apitoken', '')
        # TODO decorator
        if not pyhabitapi.login(uuid, apitoken):
            return redirect(url_for('buy_gems'))
        ret = pyhabitapi.buy_gems(uuid, apitoken, gems)
        if ret == True:
            flash('Gems bought', 'success')
            return redirect(url_for('index'))
        elif ret is not False:
            flash('Unknown error', 'danger')

    return render_template('actions/buy_gems.html',
                           habit_link=app.config['HABIT_LINK'])

@app.route('/gems/sell', methods=['GET', 'POST'])
def sell_gems():
    if request.method == 'POST':
        if request.form.get('uuid', '') == '':
            flash('No UUID', 'danger')
            return redirect(url_for('sell_gems'))
        if request.form.get('apitoken', '') == '':
            flash('No API token', 'danger')
            return redirect(url_for('sell_gems'))
        if request.form.get('gems') == '':
            flash('Bad gem input', 'danger')
            return redirect(url_for('sell_gems'))

        try:
            gems = int(request.form.get('gems', 0))
        except:
            flash('Bad gems input', 'danger')
            return redirect(url_for('sell_gems'))
        if gems < 1:
            flash('Bad gems input', 'danger')
            return redirect(url_for('sell_gems'))

        uuid = request.form.get('uuid', '')
        apitoken = request.form.get('apitoken', '')
        # TODO decorator
        if not pyhabitapi.login(uuid, apitoken):
            return redirect(url_for('sell_gems'))
        ret = pyhabitapi.sell_gems(uuid, apitoken, gems)
        if ret == True:
            flash('Gems sold', 'success')
            return redirect(url_for('index'))
        elif ret is not False:
            flash('Unknown error', 'danger')


    return render_template('actions/sell_gems.html',
                           habit_link=app.config['HABIT_LINK'])


@app.route('/gold/transfer', methods=['GET', 'POST'])
def transfer_gold():
    if request.method == 'POST':
        if request.form.get('uuid', '') == '':
            flash('No UUID', 'danger')
            return redirect(url_for('transfer_gold'))
        if request.form.get('apitoken', '') == '':
            flash('No API token', 'danger')
            return redirect(url_for('transfer_gold'))
        if request.form.get('receiver_uuid', '') == '':
            flash('No receiver UUID', 'danger')
            return redirect(url_for('transfer_gold'))
        if request.form.get('gold') == '':
            flash('Bad gold input', 'danger')
            return redirect(url_for('transfer_gold'))
        try:
            gold = float(request.form.get('gold', 0))
        except:
            flash('Bad gold input', 'danger')
            return redirect(url_for('transfer_gold'))
        if gold < 0:
            flash('Bad gold input', 'danger')
            return redirect(url_for('transfer_gold'))

        uuid = request.form.get('uuid', '')
        apitoken = request.form.get('apitoken', '')
        receiver_uuid = request.form.get('receiver_uuid', '')

        # TODO decorator
        if not pyhabitapi.login(uuid, apitoken):
            return redirect(url_for('transfer_gold'))

        ret = pyhabitapi.transfer_gold(uuid, apitoken, receiver_uuid, gold)
        if ret == True:
            flash('Gold transfered', 'success')
            return redirect(url_for('index'))
        elif ret is not False:
            flash('Unknown error', 'danger')
    return render_template('actions/transfer_gold.html',
                           habit_link=app.config['HABIT_LINK'])


if __name__ == "__main__":
    app.run()
