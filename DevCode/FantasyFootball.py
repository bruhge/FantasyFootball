from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
import pandas as pd
import sqlite3

class Database():

    def create():
        db = sqlite3.connect("fantasy.db")
        db.execute("CREATE TABLE IF NOT EXISTS players (id PRIMARY KEY NOT NULL, player NOT NULL, position NOT NULL, team NOT NULL)")
        for row in pd.read_csv('Playerlist.csv', encoding="cp1252").values:
            number, player, position, team = row
            db.execute("INSERT INTO players VALUES(?, ?, ?, ?)", (number, player, position, team))
        db.commit()
        db.close()

    def delete():
        db = sqlite3.connect("fantasy.db")
        db.execute("DROP TABLE players")
        db.commit()
        db.close()
        

class PlayerListButton(ListItemButton):
    pass

class PlayerList(BoxLayout):
    player_name_text_input = ObjectProperty()
    position_text_input = ObjectProperty()
    team_text_input = ObjectProperty()
    player_list = ObjectProperty()

    def filter_player(self):
        player = self.player_name_text_input.text
        position = self.position_text_input.text
        team = self.team_text_input.text

        if player != '':
            player = " WHERE player LIKE '%" + player + "%'"

        if position != '':
            if player == '':
                position = " WHERE position = '" + position + "'"
            else:
                position = " AND position = '" + position + "'"

        if team != '':
            if player == '' and position == '':
                team = " WHERE team LIKE '%" + team + "%'"
            else:
                team = " AND team LIKE '%" + team + "%'"

        db = sqlite3.connect("fantasy.db")
        cursor = db.execute("SELECT * FROM players" + player + position + team + " LIMIT 40")
        row = cursor.fetchall()
        cursor.close()
        db.close()
        
        self.player_list.adapter.data = []
        for i in row:
            self.player_list.adapter.data.extend([str(i)])
            self.player_list._trigger_reset_populate()

    def delete_player(self):
        if self.player_list.adapter.selection:
            selection=self.player_list.adapter.selection[0].text
            print(selection)
            number, name, position, team = selection.split(',')
            print(number)
            number = number[1::]
            print(number)
            db = sqlite3.connect("fantasy.db")
            delete = "delete from players where id = {}".format(number)
            print(delete)
            db.execute(delete)
            db.commit()
            db.close()

    def myPlayer(self):
        pass
        

class FantasyApp(App):
    def build(self):
        return PlayerList()


Database.delete()
Database.create()
FantasyApp().run()
