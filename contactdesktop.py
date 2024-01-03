###############################################################################
#            Voici les imports des modules et librairies python               #
###############################################################################
import tkinter as tk
from tkinter import messagebox
import os
import datetime

###############################################################################
#      Voici les variables et mise en place de l'encodage par défaut          #
###############################################################################
ligne = 0
notes = ""

os.environ["PYTHONUTF8"] = "1"  # activer l'encodage UTF-8 par défaut.

###############################################################################
#           Voici les fonctions pour definir les actions du menu              #
###############################################################################


def check_repertoire():
    lignes_non_conf = []
    with open('repertoire.txt', 'r', encoding="utf-8") as fichier:
        lines = fichier.readlines()
        if not lines:
            print("Le fichier répertoire.txt est vide")
            messagebox.showwarning("Warning", "Le fichier répertoire.txt est vide.")
        for line in lines:
            if line != "\n":
                linesplit = line.strip().split('@')
                if len(linesplit) != 4:
                    print(f"Warning : ligne invalide dans le fichier répertoire.txt : {line}")
                    lignes_non_conf.append("Ligne non conforme dans le fichier répertoire.txt - " + line)

        if lignes_non_conf:
            try:
                with open(f'logs/logs_du_{datetime.date.today()}.txt', 'w') as logs:
                    logs.writelines(lignes_non_conf)
            except Exception as exeption:
                print(f"Erreur lors de la création du fichier logs : {exeption}")

            messagebox.showwarning("Warning",
                                   "Une ou plusieurs lignes dans le fichier répertoire sont invalides. "
                                   "Merci de les supprimer ou les remplacer pour que le programme puisse fonctionner.")
            exit()


def trier_contact(contacts):
    """
    trier_contact(contacts) permet de trier les contacts par nom, prénom ou par numéro.
    """
    ordre_de_tri = tri_var.get()
    if ordre_de_tri == 'nom':
        contacts.sort(key=lambda x: x[1])
    elif ordre_de_tri == 'prenom':
        contacts.sort(key=lambda x: x[2])
    elif ordre_de_tri == 'numero':
        contacts.sort(key=lambda x: x[3])


def ajoutercontact(nom, prenom, tel):
    """
    ajoutercontact(nom,prénom,tel) qui prend en paramètre 3 chaines de caractères avec tkinter.
     La fonction permet d'ajouter la ligne dans repertoire.txt avec le nouveau contact.
    """
    # Vérification du numéro de téléphone
    if not tel.isdigit():
        messagebox.showerror("Erreur", "Le numéro de téléphone doit être composé uniquement de chiffres.")
        return
    # lecture du contenu du fichier repertoire.txt pour obtenir le nombre de contacts déjà existants
    with open('repertoire.txt', 'r', encoding="utf-8") as fichier:
        lignes = fichier.readlines()

        num_max_contacts = 0
        for line in lignes:
            if line.strip() != "":
                id_contact = int(line.split(':')[0])
                if id_contact > num_max_contacts:
                    num_max_contacts = id_contact

    # création de la nouvelle ligne à ajouter avec le numéro du contact ainsi que des informations du contact
    # (séparés par des "@")
    numero_contact = str(num_max_contacts + 1)
    contact = numero_contact + ":@" + nom + "@" + prenom + "@" + tel

    # ajout de la nouvelle ligne dans le fichier repertoire.txt
    with open('repertoire.txt', 'a', encoding="utf-8") as fichier:
        fichier.write("\n" + contact)
    # effacement des champs de saisie dans la fenêtre Tkinter et affichage de la liste des contacts mise à jour
    nom_entry.delete(0, tk.END)
    prenom_entry.delete(0, tk.END)
    tel_entry.delete(0, tk.END)
    affichertout()


def affichercontact(nom, prenom, tel, notes=""):
    """
    affichercontact(n,p,t,notes="") qui prend en paramètre 3 chaines de caractères et une note optionnelle.
    La fonction permet d'afficher proprement le contact et sa petite note personnalisée si elle existe.
    """
    contacts_text.delete(1.0, tk.END)
    contacts_text.insert(tk.END, f"################################################################################\n                       Fiche d'information de {nom.upper()} :      \n - Nom : {nom} \n - Prénom : {prenom.upper()} \n - Téléphone : {tel}  \n - Notes : {notes}      \n###############################################################################", "blanc")


def notes_boutton(entry_text):
    """
    notes_boutton(entry_text) qui prend en paramètre entry_text qui est une chaine de caractère permet de vérifier si la forme de la note est correcte.
    Si ce n'est pas le cas elle explique à l'utilisateur les formes à utiliser puis il va séparer le numéro du contact avec la note et la renvoyer à la fonction "sauvegardernote(num,note)".
    """
    if not (":" in entry_text or "-" in entry_text):
        messagebox.showinfo("Info", "Pour ajouter une note à un contact il vous faut utiliser une des formes suivantes : \n numéro_du_contact:note\n numéro_du_contact-note")
    else:
        if ":" in entry_text:
            separateur = ":"
        else:
            separateur = "-"
        number, note = entry_text.split(separateur, maxsplit=1)
        if not number.isdigit():
            messagebox.showinfo("Info", "Le nombre doit être un entier.")
            return
        sauvegardernote(number.strip(), note.strip())


def sauvegardernote(num,note):
    """
    sauvegardernote(num, note) qui prend en paramètre une chaine de caractère « num » contenant le numéro du contact et une autre chaine de caractère « note » qui contient la note du contact.
    Elle va ensuite sauvegarder cette note dans le fichier « notes_{nom}_{prenom}.txt » pour qu'elle puisse être ré-utilisée par la suite.
    """
    nom, prenom, tel = lirecontact(num)
    notes_file = f"notes/notes_{nom.lower()}_{prenom.lower()}.txt"
    with open(f'{notes_file}', 'w', encoding="utf-8") as notes_fichier:
        notes_fichier.write(note.strip() + "\n")
    note_entry.delete(0, tk.END)
    affichercontact(nom, prenom, tel, note)

def lirecontact(n):
    """
    lirecontact(n) qui prend en paramètre un nombre entier « n » et qui va retourner le nom, prénom et téléphone contenu dans la ligne du fichier repertoire.txt au contact correspondant à ce numéro.
    Il l'affichera ensuite à l'aide de la fonction "affichercontact".
    """
    try:
        num = int(n.strip())
        contacts_text.delete(1.0, tk.END)
        with open('repertoire.txt', 'r', encoding="utf-8") as fichier:
            lines = fichier.readlines()

        if num <= len(lines):
            for line in lines:
                if line != "\n":
                    linesplit = line.split(':')
                    tab = linesplit[0]
                    if tab == n:
                        linesplit = line.split('@')
                        nom = linesplit[1]
                        prenom = linesplit[2]
                        tel = linesplit[3].strip()
                        notes_file = f"notes/notes_{nom.lower()}_{prenom.lower()}.txt"
                        notes = ""
                        if os.path.exists(notes_file):
                            with open(notes_file, 'r', encoding="utf-8") as notes_fichier:
                                notes = notes_fichier.read()
                        print(
                            f"Contact n°{num} :\n- Nom : {nom} \n- Prénom : {prenom.upper()} \n- Téléphone : {tel}\n- Notes : {notes}\n")
                        affichercontact(nom, prenom, tel, notes)
                        return nom, prenom, tel
                    else:
                        continue
            else:
                messagebox.showerror("Erreur", "Le contact n'existe pas.")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre.")


def affichertout(sort_order='nom'):
    """
    affichertout() fonction qui affiche entièrement et proprement l’ensemble des contacts contenus dans le fichier repertoire.txt
    avec un ordre de tri spécifié par l'utilisateur

    Args:
    sort_order (str): L'ordre de tri souhaité, par défaut trié par le nom

    """
    contacts_text.delete(1.0, tk.END)
    with open('repertoire.txt', 'r', encoding="utf-8") as fichier:
        lines = fichier.readlines()
        contacts = []
        for line in lines:
            if line != "\n":
                tab = line.split('@')
                id = tab[0]
                nom = tab[1]
                prenom = tab[2]
                tel = tab[3]
                contacts.append((id, nom, prenom, tel))
        trier_contact(contacts)
        for contact in contacts:
            id, nom, prenom, tel = contact
            contacts_text.insert(tk.END, f"{id} {nom} {prenom} {tel}\n", "blanc")


def recherche(texte):
    """
    rechercher(texte) qui prend en paramètre une chaine de caractère et qui va chercher la présence de ce texte dans le fichier repertoire.txt .
    Elle va alors retourner la liste des numéros de lignes qui contiennent le text et les afficher sur l'interface tkinter.
    """
    contacts = []
    liste = []
    with open('repertoire.txt', 'r', encoding="utf-8") as fichier:
        lines = fichier.readlines()
        for indice, line in enumerate(lines): #cette boucle "for" itère/va se répéter pour chaque ligne du fichier "repertoire.txt" stockée dans la liste "lines", tout en gardant une trace de l'indice de chaque ligne grâce à la fonction "enumerate()".
            if texte in line.lower():  # Convertir la ligne du fichier en minuscules et tester si le texte est dans la ligne
                liste.append(indice + 1)
                tab = line.strip().split('@')
                contacts.append((tab[0], tab[1], tab[2], tab[3]))
    if len(contacts) == 0 or len(liste) == 0:
        print("\nRésultat de la recherche: Aucun contact trouvé.")
        messagebox.showinfo("Info", "Aucun contact trouvé.")
    else:
        trier_contact(contacts)
        # afficher les contacts triés
        print("\nRésultat de la recherche: \n" + "Les numéros des lignes : "+ str(liste) + "\nLes informations des lignes : " + str(contacts))
        contacts_text.delete(1.0, tk.END)
        for contact in contacts:
            ##### colorié le text correspondant en rouge : #####
            contact_info = f"{contact[0]} {contact[1]} {contact[2]} {contact[3]}\n"
            start_idtxt = 0
            while True: #Dans la boucle while, la méthode find est utilisée pour rechercher la prochaine apparition de "texte" dans la chaîne contact_info, en commençant à la position start_idtxt.
                index_texte = contact_info.lower().find(texte, start_idtxt)  #index_texte fait référence à l'index de la sous-chaîne texte dans la chaîne contact_info. Si texte est trouvé, l'index du premier caractère de la sous-chaîne est retourné, qui est stocké dans index_texte. Si texte n'est pas trouvé, -1 est retourné.
                if index_texte == -1:
                    contacts_text.insert(tk.END, contact_info[start_idtxt:], "blanc")
                    break
                # index_texte est ensuite utilisé pour insérer le texte non correspondant précédent et le texte correspondant avec une balise de style spéciale dans le widget contacts_text à l'aide de la méthode d'insertion.
                contacts_text.insert(tk.END, contact_info[start_idtxt:index_texte], "blanc")
                contacts_text.insert(tk.END, contact_info[index_texte:index_texte+len(texte)], "rouge_gras")
                start_idtxt = index_texte + len(texte) #Le start_idx est mis à jour en index_texte + len(texte) afin que la recherche de la prochaine occurrence de texte dans contact_info commence après la correspondance en cours.
            contacts_text.insert(tk.END, "\n")
    return liste


def supprimerligne(n):
    """
    supprimerligne(n) qui prend en paramètre un nombre entier « n » et qui va supprimer dans le fichier repertoire.txt la ligne correspondant à ce numéro.
    """
    try:
        lignesup = int(n.strip())
        with open('repertoire.txt', 'r') as fileread:
            lines = fileread.readlines()

        if lignesup <= len(lines):
            new_lines = []
            for line in lines:
                if line != "\n":
                    linesplit = line.split(':')
                    tab = linesplit[0]
                    if tab != n:
                        new_lines.append(line)
                    else:
                        continue

            with open('repertoire.txt', 'w') as filewrite:
                filewrite.writelines(new_lines)

            supprimerligne_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Le contact n'existe pas.")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre.")


###############################################################################
#                    Création de la fenêtre principale                        #
###############################################################################
root = tk.Tk()
root.title("Liste de Contacts")
check_repertoire()

###############################################################################
#                           Création des widgets                              #
###############################################################################
result_label = tk.Label(root, text="")

nom_label = tk.Label(root, text="Nom:")
prenom_label = tk.Label(root, text="Prénom:")
tel_label = tk.Label(root, text="Téléphone:")

trier_par = tk.Label(root, text="Trier par:")
lire_label = tk.Label(root, text="Numéro du contact à lire:")
recherche_label = tk.Label(root, text="Rechercher:")
supprimerligne_label = tk.Label(root, text="Supprimer la ligne:")
note_label = tk.Label(root, text="Note:")

nom_entry = tk.Entry(root)
prenom_entry = tk.Entry(root)
tel_entry = tk.Entry(root)
lire_entry = tk.Entry(root)
recherche_entry = tk.Entry(root)
supprimerligne_entry = tk.Entry(root)
note_entry = tk.Entry(root, width=30)

ajouter_button = tk.Button(root, text="Ajouter", command=lambda: ajoutercontact(nom_entry.get().replace(" ", ""), prenom_entry.get().replace(" ", ""), tel_entry.get().replace(" ", "")))
supprimerligne_button = tk.Button(root, text=" Supprimer ", command=lambda: supprimerligne(supprimerligne_entry.get()))
note_button = tk.Button(root, text="Sauvegarder Note", command=lambda: notes_boutton(note_entry.get()))
lire_button = tk.Button(root, text="   Afficher   ", command=lambda: lirecontact(lire_entry.get()))
affichertout_button = tk.Button(root, text="Afficher tout", command=affichertout)
recherche_button = tk.Button(root, text="Rechercher", command=lambda: recherche(recherche_entry.get().strip().lower()))

tri_var = tk.StringVar(value='nom')

nom_rb = tk.Radiobutton(root, text='Par nom', variable=tri_var, value='nom', command=affichertout)
prenom_rb = tk.Radiobutton(root, text='Par prénom', variable=tri_var, value='prenom', command=affichertout)
num_tel_rb = tk.Radiobutton(root, text='Par numéro', variable=tri_var, value='numero', command=affichertout)

contacts_text = tk.Text(root)
contacts_text.configure(background='black')
contacts_text.tag_config("blanc", foreground="white")
contacts_text.tag_config("rouge_gras", foreground="red", font=("TkDefaultFont", 10, "bold"))
contacts_text.grid(row=0, column=3, rowspan=12)

trier_par.grid(row=0, column=0)
nom_rb.grid(row=1, column=0, sticky='w')
prenom_rb.grid(row=1, column=1, sticky='w')
num_tel_rb.grid(row=1, column=2, sticky='w')
result_label.grid(row=1, column=0, columnspan=3)
note_label.grid(row=7, column=0)
note_entry.grid(row=7, column=1, columnspan=1)

note_button.grid(row=8, column=1)
#ou : note_button.grid(row=7, column=2)

nom_label.grid(row=2, column=0)
nom_entry.grid(row=2, column=1)
prenom_label.grid(row=3, column=0)
prenom_entry.grid(row=3, column=1)
tel_label.grid(row=4, column=0)
tel_entry.grid(row=4, column=1)
ajouter_button.grid(row=5, column=0, columnspan=3, pady=10)

lire_label.grid(row=9, column=0)
lire_entry.grid(row=9, column=1)
lire_button.grid(row=9, column=2, pady=10)

affichertout_button.grid(row=11, column=0, columnspan=3, pady=10)

recherche_label.grid(row=6, column=0)
recherche_entry.grid(row=6, column=1)
recherche_button.grid(row=6, column=2, pady=10)

supprimerligne_label.grid(row=10, column=0)
supprimerligne_entry.grid(row=10, column=1)
supprimerligne_button.grid(row=10, column=2, pady=10)

result_label.grid(row=11, column=0, columnspan=3)

root.mainloop()
