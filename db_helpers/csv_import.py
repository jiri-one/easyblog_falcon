#!/usr/bin/python3
# -*- coding: utf-8 -*-
from rethinkdb import RethinkDB
import csv
from html import unescape

r = RethinkDB()
conn = r.connect( "192.168.222.20", 28015).repl()
topics = r.db("devel").table("topics")
posts = r.db("devel").table("posts")

with open('zapisky.csv', encoding="utf-8") as csvfile:
    posts.delete().run(conn)
    reader = 0
    fieldnames = ['cislo', 'url', 'nadpis', 'obsah', 'zadano_kdy', 'pocet_komentaru', 'kategorie']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=',')
    sorted_reader = sorted(reader, key=lambda row: row["zadano_kdy"], reverse=False)
    for row in sorted_reader[:-1]: 
        posts.insert({
            'comments': 0,
            'when': row['zadano_kdy'],
            'url': {"cze": row['url']}, #tady uvidíme, zda se dá pak přidávat další do slovníku, ale předpokládám, že ano (i další tři položky)
            'header': {"cze": unescape(row['nadpis'])}, 
            'content': {"cze": unescape(row['obsah'])},
            'topics': {"cze": row['kategorie']}
        }).run(conn)

with open('kategorie.csv', encoding="utf-8") as csvfile:
    topics.delete().run(conn)
    reader = 0
    fieldnames = ['kategorie', 'popis', 'cislo', 'url_kategorie']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')
    for row in list(reader)[1:]:
        info = topics.insert({
            'order': row['cislo'],
            'topic': {"cze": row['kategorie'], "eng": ""},
            'url': {"cze": row['url_kategorie'], "eng": ""},
            'description': {"cze": row['popis'], "eng": ""}
            }).run(conn)

# get from url
#cursor = posts.filter(r.row["url"]["cze"] == "predatori").run(conn)

# add or update; in this case add english version of url
#posts.filter(r.row["url"]["cze"] == "predatori").update({"url": {"eng": "predators"}}).run(conn)

# just add is with .append
# delete is with .delete


#fieldnames = ['cislo', 'url', 'nadpis', 'obsah', 'zadano_kdy', 'pocet_komentaru', 'kategorie']        
#posts.delete().run(conn)
#reader = 0
#csvfile = open('zapisky.csv', encoding="utf-8")
#reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')
#sorted_reader = sorted(reader, key=lambda row: row["zadano_kdy"], reverse=False)
#for row in sorted_reader[:-1]: 
    #zapisky.insert({'comments': row['pocet_komentaru'], 'when': row['zadano_kdy'], 'url': row['url'], 'header': row['nadpis'], 'content': row['obsah'], 'categories': row['kategorie']})
   
### tady zacinaji dalsi verze, ktere nefungovaly!!!    
    #with open('/home/klerik/Downloads/muj_blog/zapisky.csv') as csvfile:
        #fieldnames = ['cislo', 'url', 'nadpis', 'obsah', 'zadano_kdy', 'pocet_komentaru', 'kategorie']
        #reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')
        #for row in reader:
            #zapisky.insert({'comments': row['pocet_komentaru'], 'when': row['zadano_kdy'], 'url': row['url'], 'header': row['nadpis'], 'content': row['obsah']})
    
    #with open('/home/klerik/Downloads/muj_blog/zapisky.csv') as csvfile:
        #reader = csv.reader(csvfile, delimiter=';')
        #sorted_reader = sorted(reader, key=lambda row: row[5], reverse=True)
        #for row in sorted_reader: 
            #zapisky.insert({'comments': row[5], 'when': row[4], 'url': row[1], 'header': row[2], 'content': row[3]})

#kategorie.search(where('url_kategorie') == 'knihy')
#zapisky.search(where("url") == "darth-plagueis-docteno")