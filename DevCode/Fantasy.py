from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.listview import ListItemButton
import pandas as pd
import sqlite3

class PlayerListButton(ListItemButton):
    pass

class PlayerList(BoxLayout):
    playerName = StringProperty('*')
    position = ObjectProperty('*')
    team = ObjectProperty('*')
    player_list = ObjectProperty()

    def populateList(self):
        db = sqlite3.connect("fantasy.db")
        db.execute("CREATE TABLE IF NOT EXISTS players (id PRIMARY KEY NOT NULL, player NOT NULL, position NOT NULL, team NOT NULL)")
        for row in pd.read_csv('Playerlist.csv', encoding="cp1252").values:
            number, player, position, team = row
            db.execute("INSERT INTO players VALUES(?, ?, ?, ?)", (number, player, position, team))
        db.commit()
        db.close()

    def filter(self):
        print(type(self.player_list))
        player = self.playerName.text
        position = self.ids['position'].text
        team = self.ids['team'].text

        if player == "*":
            player=""
        else:
            player = "WHERE player LIKE '%" + player + "%'"

        if position == "*":
            position = ""
        elif player != "":
            position = " AND position = '" + position + "'"
        else:
            position = "WHERE position = '" + position + "'"

        if team == "*":
            team = ""
        elif player != "" or position != "":
            team = " AND team = '" + team + "'"
        else:
            team = "WHERE team = '" + team +"'"
        db = sqlite3.connect('fantasy.db')
        cursor = db.execute("SELECT * FROM players " + player + position + team + " LIMIT 40")
        row = cursor.fetchall()
        db.close()
        for i in row:
            self.player_list.adapter.data.extend([i])
            self.player_list._triger_reset_populate()
        


class FantasyApp(App):
    def build(self):
        #PlayerList().populateList()
        return PlayerList()

#db = sqlite3.connect("fantasy.db")
#db.execute("DROP TABLE players")
#db.commit()
#db.close()
FantasyApp().run()

