import random
import pygame

pygame.init()

LARGEUR = 1300
HAUTEUR = 700
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Génération de molécule")

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (70, 70, 70)

imageclasse_originale = pygame.image.load("img/classe.jpg")
font = pygame.font.Font(None, 36)
petite_font = pygame.font.Font(None, 28)
statut_font = pygame.font.Font(None, 24)
titre_font = pygame.font.Font(None, 46)

couleur_atome = {
    "H": (255, 255, 255),
    "C": (0, 0, 0),
    "N": (110, 140, 210),
    "O": (210, 100, 100)
}

atome = {"H": (1, False), "O": (2, True), "N": (3, True), "C": (4, True)}
atome2 = {"O": (2, True), "N": (3, True), "C": (4, True)}
MAX_ATOMES = 30
ZONE_MOLECULE_HAUT = 230
ORDRE_ATOMES = ["H", "O", "N", "C"]
VALENCES = {"H": 1, "O": 2, "N": 3, "C": 4}


def atomeDispo(molecule):
    nb = 0
    for i in range(len(molecule)):
        nb += molecule[i][1]

    return nb


def listeAtomesCrea(atome):
    liste = []

    for cle in atome.keys():
        if cle == "H":
            nb = 10
        elif nb == "O":
            nb = 2
        else:
            nb = 1
        for i in range(nb):
            liste.append(cle)

    return liste


def calculIndice(molecule, indiceCourant):
    assert type(molecule) == list, "Erreur"
    estPasse = False

    while molecule[indiceCourant][1] == 0:
        indiceCourant += 1

        if indiceCourant >= len(molecule) and estPasse == False:
            estPasse = True
            indiceCourant = 0
        elif estPasse == True and indiceCourant >= len(molecule):
            assert False, "Erreur sur l'indice !"

    return indiceCourant


def cree_molecule(atome):
    assert type(atome) == dict, "Erreur !"
    molecule = []
    indice = 0

    atome_base = random.choice(list(atome2.keys()))
    molecule.append([atome_base, atome2[atome_base][0]])
    liaison_disponible = True

    listeAtomes = listeAtomesCrea(atome)

    while liaison_disponible == True:
        atome_choisi = random.choice(listeAtomes)
        molecule.append([atome_choisi, atome[atome_choisi][0] - 1])
        indice = calculIndice(molecule, indice)

        if atome[atome_choisi][0] >= 2:
            molecule[indice][1] += -1
            indice += 1
        else:
            molecule[indice][1] += -1

        if atomeDispo(molecule) == 0 or len(molecule) >= MAX_ATOMES:
            liaison_disponible = False

        print(molecule)
    return molecule


def Formulebrut(molecule):
    assert type(molecule) == list, "Erreur !"
    formule_brut = []
    for i in range(len(molecule)):
        for j in range(len(molecule)):
            if type(molecule[i][j]) == str:
                formule_brut.append(molecule[i][j])
    assert type(formule_brut)
    return formule_brut


def compter_atomes(molecule_affichee: list) -> dict:  # Axel
    """Compte le nombre de H, O, N et C présents dans la molécule affichée."""
    compteur = {"H": 0, "O": 0, "N": 0, "C": 0}

    for atome_courant in molecule_affichee:
        symbole = atome_courant[0]
        compteur[symbole] += 1

    return compteur


def formule_molecule(molecule_affichee: list) -> str:  # Axel
    """Construit la formule brute de la molécule à partir des atomes comptés."""
    compteur = compter_atomes(molecule_affichee)
    morceaux = []

    if compteur["C"] > 0:
        ordre = ["C", "H", "N", "O"]
    else:
        ordre = ["H", "N", "O"]

    for symbole in ordre:
        nombre = compteur[symbole]
        if nombre > 0:
            morceaux.append(symbole)
            if nombre > 1:
                morceaux.append(str(nombre))

    return "".join(morceaux)


def compter_depuis_formule(formule: str) -> dict:  # Axel
    """Lit une formule brute et retourne le nombre de chaque type datome."""
    compteur = {"H": 0, "O": 0, "N": 0, "C": 0}
    index = 0
    
    while index < len(formule):
        symbole = formule[index]
        index += 1
        nombre = ""

        while index < len(formule) and formule[index].isdigit():
            nombre += formule[index]
            index += 1

        if symbole in compteur:
            if nombre == "":
                compteur[symbole] += 1
            else:
                compteur[symbole] += int(nombre)

    return compteur


def valider_formule(formule: str) -> str:  # Axel
    """Retourne si une formule est valide ou impossible selon les règles choisies."""
    compteur = compter_depuis_formule(formule)
    c = compteur["C"]
    h = compteur["H"]
    n = compteur["N"]

    dbe = c - h / 2 + n / 2 + 1
    if dbe < 0:
        return "molécule impossible : DBE négatif"

    total_valence = 0
    degres = []

    for symbole in ORDRE_ATOMES:
        nombre = compteur[symbole]
        valence = VALENCES[symbole]
        total_valence += nombre * valence

        for _ in range(nombre):
            degres.append(valence)

    if total_valence % 2 != 0:
        return "molécule impossible : valences impossibles"

    if degres == []:
        return "molécule impossible : structure de Lewis impossible"

    degre_max = max(degres)
    if degre_max > total_valence - degre_max:
        return "molécule impossible : structure de Lewis impossible"

    return "valide"


def calculer_positions_molecule(molecule_affichee: list) -> list:  # Axel
    """Calcule les positions des atomes pour un affichage en zigzag sur plusieurs lignes."""
    marge_x = 140
    marge_y = ZONE_MOLECULE_HAUT - 10
    espace_x = 95
    espace_y = 190
    decalage_y = 40
    max_par_ligne = 10
    positions = []

    for i in range(len(molecule_affichee)):
        ligne = i // max_par_ligne
        colonne = i % max_par_ligne

        if ligne % 2 == 0:
            colonne_affichage = colonne
        else:
            colonne_affichage = max_par_ligne - 1 - colonne

        position_x = marge_x + colonne_affichage * espace_x
        position_y = marge_y + ligne * espace_y

        if colonne % 2 == 0:
            position_y -= decalage_y
        else:
            position_y += decalage_y

        positions.append((position_x, position_y))

    return positions


def afficher_interface(molecule_affichee: list) -> None:  # Axel
    """Affiche les panneaux d'information, la formule brute et le verdict de validation."""
    compteur = compter_atomes(molecule_affichee)
    formule = formule_molecule(molecule_affichee)
    validation = valider_formule(formule)

    pygame.draw.rect(fenetre, BLANC, (20, 20, 470, 100))
    pygame.draw.rect(fenetre, NOIR, (20, 20, 470, 100), 2)
    pygame.draw.rect(fenetre, BLANC, (1010, 20, 250, 160))
    pygame.draw.rect(fenetre, NOIR, (1010, 20, 250, 160), 2)

    texte_titre = titre_font.render("Génération de molécule", True, NOIR)
    fenetre.blit(texte_titre, (35, 30))

    texte_info = petite_font.render("Espace : nouvelle molécule", True, NOIR)
    fenetre.blit(texte_info, (35, 75))

    texte_nombre = petite_font.render("Nombre d'atomes : " + str(len(molecule_affichee)), True, NOIR)
    fenetre.blit(texte_nombre, (35, 100))

    texte_nom = petite_font.render("Formule brute = " + formule, True, NOIR)
    rectangle_nom = texte_nom.get_rect(center=(750, 65))
    fenetre.blit(texte_nom, rectangle_nom)

    texte_validation = statut_font.render(validation, True, NOIR)
    rectangle_validation = texte_validation.get_rect(center=(750, 95))
    fenetre.blit(texte_validation, rectangle_validation)

    texte_legende = font.render("Légende", True, NOIR)
    fenetre.blit(texte_legende, (1080, 30))

    for i in range(len(ORDRE_ATOMES)):
        symbole = ORDRE_ATOMES[i]
        y = 75 + i * 25

        pygame.draw.circle(fenetre, couleur_atome[symbole], (1040, y), 10)
        pygame.draw.circle(fenetre, NOIR, (1040, y), 10, 1)

        texte_legende_atome = petite_font.render(symbole + " : " + str(compteur[symbole]), True, NOIR)
        fenetre.blit(texte_legende_atome, (1060, y - 10))


def afficher_molecule(molecule_affichee: list) -> None:  # Axel
    """Dessine les liaisons et les atomes de la molécule dans la fenêtre pygame."""
    rayon = 30
    positions = calculer_positions_molecule(molecule_affichee)

    for i in range(1, len(positions)):
        pygame.draw.line(fenetre, GRIS, positions[i - 1], positions[i], 5)

    for i in range(len(molecule_affichee)):
        symbole = molecule_affichee[i][0]
        position_x, position_y = positions[i]
        couleur = couleur_atome[symbole]

        pygame.draw.circle(fenetre, NOIR, (position_x, position_y), rayon + 3)
        pygame.draw.circle(fenetre, couleur, (position_x, position_y), rayon)

        if symbole == "C":
            couleur_texte = BLANC
        else:
            couleur_texte = NOIR

        texte = font.render(symbole, True, couleur_texte)
        rectangle_texte = texte.get_rect(center=(position_x, position_y))
        fenetre.blit(texte, rectangle_texte)


molecule = cree_molecule(atome)
print(molecule)

fin = False
while fin == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                molecule = cree_molecule(atome)
                print(molecule)

    taille_fenetre = fenetre.get_size()
    imageclasse = pygame.transform.scale(imageclasse_originale, taille_fenetre)

    fenetre.fill(BLANC)
    fenetre.blit(imageclasse, (0, 0))
    afficher_interface(molecule)
    afficher_molecule(molecule)
    pygame.display.flip()

pygame.quit()
