import tkinter as tk
import tkinter.filedialog
import xmlWIKI
import os
import sys
from xmlWIKI import TextRedirector
import fnmatch
import tkinter.messagebox as messagebox
import wikipedia

class XMLCreatorGUI:
    def __init__(self, master):
        global languages, language_codes

        self.master = master
        self.master.title("XML Creator")
        self.master.geometry("1360x768")

        self.game_folder_var = tk.StringVar()
        self.game_folder_var.set("C:/wamp64/www/PythonXMLCreator/test")
        self.xml_file_var = tk.StringVar()
        self.xml_file_var.set("C:/wamp64/www/PythonXMLCreator/games.xml")

        #languages settings
        self.language_var = tk.StringVar()
        self.language_var.set("English")

        # Créer une frame pour les labels et les entrées
        self.label_frame = tk.LabelFrame(self.master, text="Options")
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        languages = ["English", "Deutsch", "Italiano", "Español", "Français"]
        language_codes = ["en", "de", "it", "es", "fr"]

        tk.Label(self.label_frame, text="Langue:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.language_option_menu = tk.OptionMenu(self.label_frame, self.language_var, *languages)
        self.language_option_menu.grid(row=9, column=1, padx=5, pady=5, sticky="w")
        self.language_option_menu.bind("<<ComboboxSelected>>", self.change_language)

        tk.Label(self.label_frame, text="Game folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.label_frame, textvariable=self.game_folder_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.label_frame, text="Browse...", command=self.browse_game_folder).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        tk.Label(self.label_frame, text="XML file:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.label_frame, textvariable=self.xml_file_var, width=50).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.label_frame, text="Browse...", command=self.browse_xml_file).grid(row=1, column=2, padx=5, pady=5, sticky="ew")


        # Créer des variables pour les cases à cocher
        self.ahk_var = tk.IntVar()
        self.bat_var = tk.IntVar()
        self.bin_var = tk.IntVar()
        self.cue_var = tk.IntVar()
        self.exe_var = tk.IntVar()
        self.iso_var = tk.IntVar()
        self.rar_var = tk.IntVar()
        self.tar_var = tk.IntVar()
        self.zip_var = tk.IntVar()

        # Créer un Frame pour regrouper le label et les cases à cocher
        self.file_type_frame = tk.Frame(self.label_frame)
        self.file_type_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Ajouter le label "Choix du type de fichiers:"
        tk.Label(self.file_type_frame, text="Choix du type de fichiers (.bat, .bin, .iso etc...) : ").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Créer les cases à cocher
        tk.Checkbutton(self.label_frame, text=".ahk", variable=self.ahk_var, command=self.update_extensions).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".bat", variable=self.bat_var, command=self.update_extensions).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".bin", variable=self.bin_var, command=self.update_extensions).grid(row=3, column=2, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".cue", variable=self.cue_var, command=self.update_extensions).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".exe", variable=self.exe_var, command=self.update_extensions).grid(row=4, column=1, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".iso", variable=self.iso_var, command=self.update_extensions).grid(row=4, column=2, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".rar", variable=self.rar_var, command=self.update_extensions).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".tar", variable=self.tar_var, command=self.update_extensions).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        tk.Checkbutton(self.label_frame, text=".zip", variable=self.zip_var, command=self.update_extensions).grid(row=5, column=2, padx=5, pady=5, sticky="w")

        # Ajouter le label "Ajouter type de fichier:"
        tk.Label(self.file_type_frame, text="Rechercher un type de fichiers spécifique :").grid(row=8, column=0, padx=5, pady=5, sticky="s")

        # Ajouter une Entry pour permettre à l'utilisateur d'ajouter manuellement un type de fichier
        self.custom_file_entry = tk.Entry(self.file_type_frame, width=10)
        self.custom_file_entry.grid(row=8, column=1, padx=5, pady=5, sticky="s")

        # Ajouter un gestionnaire d'événements pour mettre à jour la liste des extensions lorsque l'utilisateur saisit une extension personnalisée
        #self.custom_file_entry.bind("<FocusOut>", self.update_custom_extension)
        self.custom_file_entry.bind("<Return>", self.update_custom_extension_and_create_xml)

        # Ajouter une nouvelle entrée pour le nom de la liste
        tk.Label(self.label_frame, text="List name:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.list_name_var = tk.StringVar()
        self.list_name_var.set("PC Games")  # Valeur par défaut
        tk.Entry(self.label_frame, textvariable=self.list_name_var, width=50).grid(row=8, column=1, padx=0, pady=5, sticky="e")


        # Créer une frame pour centrer le bouton "Create XML"
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=2, column=1)
        tk.Button(button_frame, text="Create XML", command=self.update_custom_extension_and_create_xml).pack()

        # Définir les colonnes pour qu'elles se dilatent lorsque la fenêtre est redimensionnée
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        # Créer un cadre pour afficher les résumés des jeux
        self.frame = tk.Frame(self.master, bd=1, relief=tk.SUNKEN)
        self.frame.grid(row=1, column=1, sticky="nsew")

        # Créer un widget Label pour le titre du cadre de texte des résumés de jeux
        self.game_label = tk.Label(self.master, text="Résumé :", font=("Helvetica", 16, "bold"))
        self.game_label.grid(row=0, column=1, sticky="nsew")

        # Créer un widget Text pour afficher les résumés des jeux
        self.text = tk.Text(self.frame, wrap=tk.WORD, width=50, height=10)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Créer un scrollbar vertical pour le widget Text
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurer le widget Text pour utiliser le scrollbar
        self.text.configure(yscrollcommand=self.scrollbar.set)

        # Créer une frame pour la console
        self.console_frame = tk.Frame(self.master)
        self.console_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        # Créer un widget Label pour le titre du cadre de texte de la console
        self.console_label = tk.Label(self.master, text="Console :", font=("Helvetica", 13, "bold"))
        self.console_label.grid(row=0, column=3, sticky="nsew")

        self.console = tk.Text(self.console_frame, wrap="word", width=60, height=10)
        self.console.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Ajouter une barre de défilement à la console
        self.scrollbar = tk.Scrollbar(self.console_frame, command=self.console.yview)
        self.scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        self.console.config(yscrollcommand=self.scrollbar.set)

        # Configurer les poids des colonnes et des lignes
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=0)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        self.label_frame.columnconfigure(1, weight=1)
        self.console_frame.columnconfigure(0, weight=1)

        # Initialiser la liste des extensions
        self.extensions = []
        self.game_files = []

    def update_game_files(self):
        # Mettre à jour la liste des fichiers en fonction des extensions sélectionnées
        file_pattern = '|'.join([f'*.{ext}' for ext in self.extensions])
        self.game_files = [os.path.join(self.game_folder_var.get(), f) for f in os.listdir(self.game_folder_var.get()) if fnmatch.fnmatch(f, file_pattern)]


    def browse_game_folder(self):
        folder_path = tkinter.filedialog.askdirectory()
        self.game_folder_var.set(folder_path)

        # Réinitialiser la liste des extensions
        self.extensions = []

        # Construire une liste d'extensions de fichiers en fonction des cases à cocher sélectionnées et de l'extension personnalisée
        if self.ahk_var.get():
            self.extensions.append('.ahk')
        if self.bat_var.get():
            self.extensions.append('.bat')
        if self.bin_var.get():
            self.extensions.append('.bin')
        if self.cue_var.get():
            self.extensions.append('.cue')
        if self.exe_var.get():
            self.extensions.append('.exe')
        if self.iso_var.get():
            self.extensions.append('.iso')
        if self.rar_var.get():
            self.extensions.append('.rar')
        if self.tar_var.get():
            self.extensions.append('.tar')
        if self.zip_var.get():
            self.extensions.append('.zip')

        custom_file_ext = self.custom_file_entry.get().strip()
        if custom_file_ext:
            # Ajouter un point devant l'extension si l'utilisateur ne l'a pas fait
            if not custom_file_ext.startswith('.'):
                custom_file_ext = '.' + custom_file_ext
            self.extensions.append(custom_file_ext)

        # Mettre à jour la liste des fichiers de jeu
        self.update_game_files()

        # Mettre à jour la liste des fichiers en fonction des extensions sélectionnées
        file_pattern = '|'.join([f'*.{ext}' for ext in self.extensions])
        self.game_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if fnmatch.fnmatch(f, file_pattern)]

    def browse_xml_file(self):
        file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".xml")
        self.xml_file_var.set(file_path)

    def update_extensions(self):
        self.extensions = []
        if self.ahk_var.get():
            self.extensions.append('.ahk')
        if self.bat_var.get():
            self.extensions.append('.bat')
        if self.bin_var.get():
            self.extensions.append('.bin')
        if self.cue_var.get():
            self.extensions.append('.cue')
        if self.exe_var.get():
            self.extensions.append('.exe')
        if self.iso_var.get():
            self.extensions.append('.iso')
        if self.rar_var.get():
            self.extensions.append('.rar')
        if self.tar_var.get():
            self.extensions.append('.tar')
        if self.zip_var.get():
            self.extensions.append('.zip')

        custom_file_ext = self.custom_file_entry.get().strip()
        if custom_file_ext:
            # Ajouter un point devant l'extension si l'utilisateur ne l'a pas fait
            if not custom_file_ext.startswith('.'):
                custom_file_ext = '.' + custom_file_ext
            self.extensions.append(custom_file_ext)

        # Mettre a jour la liste des fichiers en fonction des extensions sélectionnées
        file_pattern = '|'.join([f'*.{ext}' for ext in self.extensions])
        self.game_files = [os.path.join(self.game_folder_var.get(), f) for f in os.listdir(self.game_folder_var.get()) if fnmatch.fnmatch(f, file_pattern)]

        # Mettre a jour la liste des fichiers de jeu
#        self.browse_game_folder()
        self.update_game_files()

    def update_custom_extension_and_create_xml(self, event=None):
        language_code = language_codes[languages.index(self.language_var.get())]
        # Récupérer le nom de la liste à partir de l'entrée

        list_name = self.list_name_var.get()

        # Mettre à jour la liste des extensions avec l'extension personnalisée
        self.update_custom_extension()

        # Créer le fichier XML et récupérer les jeux
        games = self.create_xml(language_code, list_name)

        # Effacer le contenu du widget Text
        self.text.delete(1.0, tk.END)

        # Ajouter les résumés des jeux dans le widget Text
        for game in games:
            summary = game['summary']
            if len(summary) > 200:
                summary = summary[:200] + '...'
            self.text.insert(tk.END, f"{game['title']}\n{summary}\n\n")

    def update_custom_extension(self, event=None):
        custom_file_ext = self.custom_file_entry.get().strip()
        if custom_file_ext:
            # Ajouter un point devant l'extension si l'utilisateur ne l'a pas fait
            if not custom_file_ext.startswith('.'):
                custom_file_ext = '.' + custom_file_ext
            self.extensions.append(custom_file_ext)

        # Mettre à jour la liste des fichiers en fonction des extensions sélectionnées
        file_pattern = '|'.join([f'*.{ext}' for ext in self.extensions])
        self.game_files = [os.path.join(self.game_folder_var.get(), f) for f in os.listdir(self.game_folder_var.get()) if fnmatch.fnmatch(f, file_pattern)]

        # Mettre à jour la liste des fichiers de jeu
        self.update_game_files()

    def change_language(self, event=None):
        language_code = language_codes[languages.index(self.language_var.get())]
        self.console.delete(1.0, tk.END)
        self.text.delete(1.0, tk.END)
        games = self.create_xml(language_code)
        # Ajouter les résumés des jeux dans le widget Text
        for game in games:
            summary = game['summary']
            if len(summary) > 200:
                summary = summary[:200] + '...'
            self.text.insert(tk.END, f"{game['title']}\n{summary}\n\n")

    def create_xml(self, language_code, list_name):

        #global languages, language_codes

        game_folder = self.game_folder_var.get()
        xml_file = self.xml_file_var.get()
        console = self.console


    # Vérifier si au moins un type de fichier est sélectionné ou si une extension personnalisée est saisie
        if not self.extensions and not self.custom_file_entry.get().strip():
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins un type de fichier ou saisir une extension personnalisée.")
            return

    # Rediriger la sortie standard vers la zone de texte de la console
        sys.stdout = TextRedirector(self.console, sys.stdout)
        sys.stderr = TextRedirector(self.console, sys.stderr)

    # Définir la langue par défaut en fonction de la langue sélectionnée par l'utilisateur
        #language = self.language_var.get()
        #language_code = language_codes[languages.index(language)]
        wikipedia.set_lang(language_code)

        print(f"Langue définie : {language_code}")  # Imprime la valeur de language_code

        # Récupérer le nom de la liste à partir de l'entrée
        list_name = self.list_name_var.get()

    # Créer le fichier XML et récupérer les jeux
        games = xmlWIKI.main(game_folder, self.extensions, xml_file, console, language_code, list_name)

    # Restaurer la sortie standard d'origine
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        return games

    # Effacer le contenu du widget Text
        self.text.delete(1.0, tk.END)

    # Ajouter les résumés des jeux dans le widget Text
        for game in games:
            summary = game['summary']
            if len(summary) > 80:
                summary = summary[:80] + '...'
            self.text.insert(tk.END, f"{game['title']}\n{summary}\n\n")

root = tk.Tk()
app = XMLCreatorGUI(root)
root.mainloop()
