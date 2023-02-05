#!/usr/bin/python3.6
import json, re, requests, sqlite3, discord, time

class Api():
    ''' Do the work against pubg.report api '''
    from bot.main import build_embed
    def getId(self, i):
        '''Get the Get the playername Counterpart'''
        url  = "https://api.pubg.report/search/" + i
        x = requests.get(url)
        z = x.text
        y = json.loads(z)
        for y in y:
            if y['shard'] == "steam":
                if y['nickname'] == i:
                    return y['id']
            return None
        return None

    def getStream(self, i):
        ''' Get the json data we need from pubg.report '''
        if i.split('.')[0] != 'account':
            id = self.getId(i)
        id = i
        if id != None:
            url = "https://api.pubg.report/v1/players/" + id + "/streams"
            x = requests.get(url)
            z = x.text
            return z

    def event(self, i, discorduser):
        '''Processes the data we got from pubg.report '''
        k = self.getStream(i)
        if k != None:
            k = json.loads(k)
            for i in iter(k):
                x = k[i]
                for item in x:
                    mmap = item['Map']
                    killer = item['Killer'] 
                    victim = item['Victim']
                    distance = item['Distance']
                    when = item['TimeEvent']
                    weapon = item['DamageCauser']
                    mode = item['Mode']
                    event = item['Event']
                    twitchID = item['TwitchID']
                    videoID = item['VideoID']
                    matchID = item['MatchID']
                    eventID = item['ID']
                    diff = item['TimeDiff']
                    # Send to build embed so we can prettyprint it to discord.
                    time.sleep(1)
                    self.build_embed(discorduser=discorduser, killer=killer, victim=victim, distance=distance, mmap=mmap, mode=mode, weapon=weapon, event=event, twitchID=twitchID, videoID=videoID, matchID=matchID, eventID=eventID, when=when, diff=diff)
        else:
            return None

    def report_register(self, author, name):
        ''' Handles the registration '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        rep_sql_reg = 'SELECT pubg_id from players WHERE discord_username ="{}"'.format(author)
        result = c.execute(rep_sql_reg)
        exist = result.fetchall()
        if len(exist) == 0:
            c.execute('INSERT INTO players VALUES("{}","{}")'.format(author, name))
            conn.commit()
            c.close()
            return True
        c.close()
        return False

    def report_unregister(self, author, name):
        ''' handles the de-registration '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        rep_sql_reg = 'SELECT pubg_id from players WHERE pubg_id ="{}"'.format(name)
        result = c.execute(rep_sql_reg)
        exist = result.fetchall()
        if len(exist) != 0:
            c.execute('DELETE from players WHERE pubg_id = "{}"'.format(name))
            conn.commit()
            c.close()
            return True
        c.close()
        return False
