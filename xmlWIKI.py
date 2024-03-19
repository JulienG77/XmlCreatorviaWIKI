import os
import wikipedia
import requests
import datetime
import tkinter as tk
from bs4 import BeautifulSoup
from bs4 import GuessedAtParserWarning
import warnings
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)
import xml.etree.ElementTree as ET


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, self.tag)
        self.widget.see("end")
        self.widget.configure(state="disabled")

#def get_file_names(directory,game_folder):
def get_file_names(directory, extensions):
    #return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1] in extensions]


def parse_info_wikipedia(page_title, language_code):
    wikipedia.set_lang(language_code)
    try:
        page = wikipedia.page(page_title)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Page ambiguë : {page_title}")
        return None
    except wikipedia.exceptions.PageError as e:
        print(f"Page non trouvée : {page_title}")
        return None

    # Extraire le titre de la page
    title = page.title

    # Extraire l'image
    img_url = page.images[0] if page.images else None

    # Extraire le résumé
    summary = page.summary


    # Extraire les informations sur le développeur et l'éditeur
    GameName = page_title
    url = 'https://fr.wikipedia.org/wiki/{}'.format(GameName)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    infobox = soup.find('div', {'class': 'infobox_v3 noarchive large'})
    infobox_data = soup.find('div', {'class': 'infobox-data'})
    developer = infobox.find('th', text='Développeur').find_next('td').text.strip()
    publisher = infobox.find('th', text='Éditeur').find_next('td').text.strip()
    genre = infobox.find('th', text='Genre').find_next('td').text.strip()
    # Extraire l'année de sortie
    release_date = infobox.find('th', text='Date de sortie').find_next('td').text.strip()
    # Nombre de Joueurs
    #num_players = infobox.find('th', text='Mode').find_next('td').text.strip()


    print('Titre :', title)
    print('Développeur :', developer)
    print('Éditeur :', publisher)
    print('Genre :', genre)
    print('Date de sortie :', release_date)
    #print('Nombre de Joueurs :', num_players)


    # Créer un dictionnaire avec les informations extraites
    info = {
        'title': title,
        'image': img_url,
        'summary': summary,
        #'num_players': num_players,
        'release_date': release_date,
        'developers': developer,
        'publisher': publisher,
        'genre': genre
    }
    return info

# OLD VERSION
#def write_to_xml(games_info, xml_file, console):
    # Créer un élément racine pour le fichier XML
#    root = ET.Element("games")

    # Créer un élément pour chaque jeu et ajouter les informations recueillies en tant qu'éléments enfants
#    for game in games_info:
#        game_elem = ET.SubElement(root, "game")
#        title_elem = ET.SubElement(game_elem, "title")
#        title_elem.text = game["title"]
#        console.insert(tk.END, f"Titre : {game['title']}\n")
#        image_elem = ET.SubElement(game_elem, "image")
#        image_elem.text = game["image"]
#        console.insert(tk.END, f"Image : {game['image']}\n")
#        summary_elem = ET.SubElement(game_elem, "summary")
#        summary_elem.text = game["summary"]
#        console.insert(tk.END, f"Résumé : {game['summary']}\n")
#        #num_players_elem = ET.SubElement(game_elem, "num_players")
        #num_players_elem.text = game["num_players"]
        #console.insert(tk.END, f"Nombre de joueurs : {game['num_players']}\n")
#        release_date_elem = ET.SubElement(game_elem, "release_date")
#        release_date_elem.text = game["release_date"]
#        console.insert(tk.END, f"Date de sortie : {game['release_date']}\n")
#        developers_elem = ET.SubElement(game_elem, "developers")
#        developers_elem.text = game["developers"]
#        console.insert(tk.END, f"Développeurs : {game['developers']}\n")
#        publisher_elem = ET.SubElement(game_elem, "publisher")
#        publisher_elem.text = game["publisher"]
#        console.insert(tk.END, f"Éditeur : {game['publisher']}\n")
#        genre_elem = ET.SubElement(game_elem, "genre")
#        genre_elem.text = game["genre"]
#        console.insert(tk.END, f"Genre : {game['genre']}\n")

    # Écrire l'arbre XML dans un fichier
#    tree = ET.ElementTree(root)
#    tree.write(xml_file, xml_declaration=True, encoding="utf-8", method="xml")

def write_to_xml(games_info, xml_file, console, list_name):

    # Créer un élément racine pour le fichier XML
    root = ET.Element("menu")

    # Créer un élément header et ajouter les éléments enfants
    header = ET.SubElement(root, "header")
    listname = ET.SubElement(header, "listname")
    listname.text = list_name  # Utiliser le paramètre list_name
    lastlistupdate = ET.SubElement(header, "lastlistupdate")
    lastlistupdate.text = datetime.datetime.now().strftime("%m-%d-%Y")
    listversion = ET.SubElement(header, "listversion")
    listversion.text = "XMLCreator " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    exporterversion = ET.SubElement(header, "exporterversion")
    exporterversion.text = "Generated by XMLCreatorWIKI"

    # Créer un élément pour chaque jeu et ajouter les informations recueillies en tant qu'éléments enfants
    for game in games_info:
        game_elem = ET.SubElement(root, "game", name=game["title"], index="", image="", enabled="1")
        description = ET.SubElement(game_elem, "description")
        description.text = game["summary"]
        cloneof = ET.SubElement(game_elem, "cloneof")
        cloneof.text = ""
        crc = ET.SubElement(game_elem, "crc")
        crc.text = ""
        manufacturer = ET.SubElement(game_elem, "manufacturer")
        manufacturer.text = game["publisher"]
        rating = ET.SubElement(game_elem, "rating")
        rating.text = ""
        year = ET.SubElement(game_elem, "year")
        year.text = game["release_date"]
        genre = ET.SubElement(game_elem, "genre")
        genre.text = game["genre"]
        developer = ET.SubElement(game_elem, "developer")
        developer.text = game["developers"]
        players = ET.SubElement(game_elem, "players")
        players.text = ""
        score = ET.SubElement(game_elem, "score")
        score.text = ""
        exe = ET.SubElement(game_elem, "exe")
        exe.text = "PC Games"
        coop = ET.SubElement(game_elem, "coop")
        coop.text = "false"
        synopsis = ET.SubElement(game_elem, "synopsis")
        synopsis.text = game["summary"]

    # Indenter l'arbre XML
    ET.indent(root, "\t")

    # Écrire l'arbre XML dans un fichier
    tree = ET.ElementTree(root)
    tree.write(xml_file, xml_declaration=True, encoding="utf-8", method="xml")


def main(game_folder, extensions, xml_file, console, language_code, list_name):
    # Récupérer la liste des fichiers dans le dossier spécifié
#    file_names = get_file_names(game_folder, extensions)
#    file_names = [os.path.basename(file_name) for file_name in game_files]
    file_names = get_file_names(game_folder, extensions)

    # Initialiser la liste des informations sur les jeux
    games_info = []

    # Effectuer une recherche Wikipedia pour chaque nom de fichier
    for file_name in file_names:
        # Diviser le nom du fichier en son nom de base et son extension
        base_name, ext = os.path.splitext(file_name)
        query = base_name.replace(" ", " ")
        #query = base_name.replace(" ", "_")
        try:
            info = parse_info_wikipedia(query, language_code)
            if info:
                # Ajouter les informations à la liste
                games_info.append(info)
                print(f"Jeu trouvé : {info['title']}")
                console.insert(tk.END, f"Jeu trouvé : {query}\n")
            else:
                print(f"Aucun résultat trouvé pour la requête de recherche : {query}")
                #console.insert(tk.END, f"Aucun résultat trouvé pour la requête de recherche : {query}\n")
        except Exception as e:
            #print(f"Erreur lors du traitement du fichier {file_name} : {e}")
            console.insert(tk.END, f"Erreur lors du traitement du fichier {file_name} : {e}\n")

    # Écrire les informations sur les jeux dans un fichier XML
    write_to_xml(games_info, xml_file, console, list_name)

    return games_info

if __name__ == "__main__":
    game_folder = "C:/wamp64/www/PythonXMLCreator/games"
    xml_file = "C:/wamp64/www/PythonXMLCreator/games.xml"
    extensions = ('.exe', '.bin', '.iso','.bat')
    console = None  # si vous n'utilisez pas de console tkinter
    main(game_folder, extensions, xml_file, console)