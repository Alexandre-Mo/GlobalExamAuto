import os
from dotenv import load_dotenv
import time
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

# Définition des variables
global_exam_section_certification = "https://exam.global-exam.com/"
global_exam_section_career = "https://business.global-exam.com/"
global_exam_section_general = "https://general.global-exam.com/"

correspondance_type_section = {1:["certification",global_exam_section_certification], 2:["career",global_exam_section_career], 3:["general",global_exam_section_general]}

grammar_url = "https://general.global-exam.com/library/study-sheets/categories/grammar"
language_functions_url = "https://general.global-exam.com/library/study-sheets/categories/language-functions"
vocabulary_url = "https://general.global-exam.com/library/study-sheets/categories/vocabulary"

correspondance_type_nbr = {1:["grammar",grammar_url], 2:["language functions",language_functions_url], 3:["vocabulary",vocabulary_url]}

global nbr_exercice
nbr_exercice = 1
global type_section
type_section = 3
global type_exercice
type_exercice = 1
global login
login = ""
global password
password = ""
global lvl
lvl = "Sort by level"
global temps
temps = 10
global lire_fiche
lire_fiche = 2
correspondance_lire_fiche = {1:["oui",True], 2:["non",False]}

# Définition des fonctions
def menu(): # Menu principal
    
    print("\n\n\n\n\n")
    print("######################################################################")
    print('#                     GLOBAL EXAM AUTO TEST MENU                     #')
    print("######################################################################")
    print("\n")

    
    # Vérifier si le fichier .env existe
    if not os.path.isfile('.env'):
        print("Le fichier .env n'existe pas. Veuillez le créer et y ajouter vos informations de connexion.")
        with open('.env', 'w') as env_file:
            global api_key
            api_key = input("Veuillez entrer votre clé API OpenAI : ")
            global login
            login = input("Veuillez entrer votre login ENT CESI : ")
            global password
            password = input("Veuillez entrer votre mot de passe ENT CESI: ")
            env_file.write(f"openai_api_key={api_key}\n")
            env_file.write(f"ent_cesi_login={login}\n")
            env_file.write(f"ent_cesi_password={password}")

    # Récupération des variables d'environnement
    load_dotenv()
    
    openai.api_key = os.environ.get("openai_api_key")
    login=os.environ.get("ent_cesi_login")
    password=os.environ.get("ent_cesi_password")

    print("Les valeurs sont : ")
    print("- Nombre d'exercice : "+str(nbr_exercice))
    print("- Type d'exercice : "+correspondance_type_nbr[int(type_exercice)][0])
    print("- Section : "+correspondance_type_section[int(type_section)][0])
    print("- Niveau : "+lvl)
    print("- Temps de résolution des exercices : "+str(temps) + " secondes")
    print("- Lire les fiches des exercices : "+correspondance_lire_fiche[int(lire_fiche)][0])
    print('\n1 = Lancement du programme | 2 = Options | 3 = Quitter')
    choix = input() # On demande à l'utilisateur de choisir une option
    if choix == '1': # Si l'utilisateur choisi l'option 1
        print('Lancement du programme')
        launch_chrome()
        global_exam_connection()
        do_exercice()
        driver.quit()
        menu()
    elif choix == '2': # Si l'utilisateur choisi l'option 2
        nombre_exercice()
        choix_type_exercice()
        choix_type_section()
        choix_lvl()
        temps_resolution()
        choix_lire_fiche()
        menu()
    elif choix == '3': # Si l'utilisateur choisi l'option 3
        print('Au revoir')


def nombre_exercice(): # Menu pour choisir le nombre d'exercice à faire
    print('Nombre d\'exercice à compléter (entre 1 et 100):')
    global nbr_exercice 
    nbr_exercice = input() # On demande à l'utilisateur de choisir un nombre d'exercice
    # si l'entré n'est pas un nombre ou ne répond pas au condition on relance le menu
    if nbr_exercice.isnumeric() == False: # Si l'entré n'est pas un nombre
        print('Veuillez entrer un nombre entre 1 et 100')
        nombre_exercice()
    elif int(nbr_exercice) < 1 or int(nbr_exercice) > 100: # Si l'entré n'est pas entre 1 et 100
        print('Veuillez entrer un nombre entre 1 et 100')
        nombre_exercice()

def choix_type_exercice(): # Menu pour choisir le type d'exercice à faire
    print('Choix du type d\'exercice à compléter (1 = grammar, 2 = language functions, 3 = vocabulary):')
    global type_exercice
    type_exercice = input() # On demande à l'utilisateur de choisir un type d'exercice
    # si l'entré n'est pas un nombre ou ne répond pas au condition on relance le menu
    if type_exercice.isnumeric() == False: # Si l'entré n'est pas un nombre
        print('Veuillez entrer un nombre entre 1 et 3')
        choix_type_exercice()
    elif int(type_exercice) < 1 or int(type_exercice) > 3: # Si l'entré n'est pas entre 1 et 3
        print('Veuillez entrer un nombre entre 1 et 3')
        choix_type_exercice()
def choix_type_section(): # Menu pour choisir la section à faire
    print('Choix de la section (1 = certification, 2 = career, 3 = general):')
    #work in progress
    print('work in progress : only general section is available for now')
    global type_section
    type_section = "3" #input() # On demande à l'utilisateur de choisir un type d'exercice
    # si l'entré n'est pas un nombre ou ne répond pas au condition on relance le menu
    if type_section.isnumeric() == False: # Si l'entré n'est pas un nombre
        print('Veuillez entrer un nombre entre 1 et 3')
        choix_type_section()
    elif int(type_section) < 1 or int(type_section) > 3: # Si l'entré n'est pas entre 1 et 3
        print('Veuillez entrer un nombre entre 1 et 3')
        choix_type_section()

def choix_lvl(): # Menu pour choisir le niveau
    print('Choix du niveau (ALL, 1, A2, B1, B2, C1, C2):')
    global lvl
    lvl = input() # On demande à l'utilisateur de choisir un type d'exercice
    # si l'entré ne correspond pas à un niveau on relance le menu
    if lvl != "ALL" and lvl != "A1" and lvl != "A2" and lvl != "B1" and lvl != "B2" and lvl != "C1" and lvl != "C2": # Si l'entré ne correspond pas à un niveau
        print('Veuillez entrer un niveau valide')
        choix_lvl()
    elif lvl =="ALL":
        lvl = "Sort by level"

def temps_resolution(): # Menu pour choisir le temps de résolution
    print('Choix du temps de résolution (en secondes):')
    global temps
    temps = input() # On demande à l'utilisateur de choisir un type d'exercice
    # si l'entré n'est pas un nombre ou ne répond pas au condition on relance le menu
    if temps.isnumeric() == False: # Si l'entré n'est pas un nombre
        print('Veuillez entrer un nombre')
        temps_resolution()

def choix_lire_fiche(): # Menu pour choisir si on lit la fiche ou non
    print('Voulez vous lire la fiche ? (1 = oui, 2 = non):')
    global lire_fiche
    lire_fiche = input() # On demande à l'utilisateur de choisir un type d'exercice
    # si l'entré n'est pas un nombre ou ne répond pas au condition on relance le menu
    if lire_fiche.isnumeric() == False: # Si l'entré n'est pas un nombre
        print('Veuillez entrer un nombre')
        lire_fiche()
    elif lire_fiche != "1" and lire_fiche != "2": # Si l'entré n'est pas entre 1 et 2
        print('Veuillez entrer un nombre entre 1 et 2')
        lire_fiche()
    

def launch_chrome(): # Lancement de chrome
    # Spécifiez le chemin vers le pilote du navigateur Chrome WebDriver
    #service = Service(executable_path='./chromedriver/chromedriver.exe') # chemin vers le driver chrome
    options = Options() # options du driver chrome
    options.add_argument("--start-maximized") # maximise la fenêtre
    options.page_load_strategy = 'eager' # permet de charger la page plus rapidement
    global mainWindow
    mainWindow = None # variable pour stocker la fenêtre principale
    # Créez une instance du navigateur Chrome
    global driver
    driver = webdriver.Chrome(options=options) # lance le driver chrome

def global_exam_connection(): # Connection à Global Exam

    url = 'https://ent.cesi.fr/accueil-apprenant' # url de l'ENT
    driver.get(url) # ouvre l'url dans le navigateur

    if driver.current_url == "https://ent.cesi.fr/accueil-apprenant": # si l'url actuel est l'url de l'ENT

        driver.get("https://moodle.cesi.fr/login/index.php?authCAS=CAS") # ouvre l'url de moodle
        mainWindow = driver.current_window_handle # stocke la fenêtre principale
        time.sleep(2)
        driver.get("https://moodle.cesi.fr/mod/lti/view.php?id=58498") # ouvre l'url de global exam

        handles = driver.window_handles # stocke les fenêtres ouvertes
        for handle in handles: # boucle pour changer de fenêtre
            if handle != mainWindow: # si la fenêtre n'est pas la fenêtre principale
                driver.switch_to.window(handle) # change de fenêtre
        
        if driver.current_url == "https://auth.global-exam.com/login" : # si l'url actuel est l'url de connection à global exam
            driver.get("https://moodle.cesi.fr/mod/lti/view.php?id=58498") # ouvre l'url de global exam
        driver.get("https://general.global-exam.com/") # ouvre l'url de global exam
        # on appui sur le bouton de type "button" contenant "General English"
        try:
            elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[span[contains(., 'General English')]]")) # on cherche l'élément par son xpath
            )
        finally:
            button = driver.find_element(By.XPATH, "//button[span[contains(., 'General English')]]").click() # on clique sur l'élément
            time.sleep(1)

    elif driver.current_url == "https://wayf.cesi.fr/login?service=https%3A%2F%2Fent.cesi.fr%2Fservlet%2Fcom.jsbsoft.jtf.core.SG%3FPROC%3DIDENTIFICATION_FRONT": # si l'url actuel est l'url de connection à l'ENT

        try:
            elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "login")) # on cherche l'élément par son id
            )
        finally:
            driver.find_element(By.ID, "login").send_keys(login) # on entre le login dans l'élément

        try:
            elem = WebDriverWait(driver, 30).until( 
            EC.presence_of_element_located((By.ID, "submit")) # on cherche l'élément par son id
            )
        finally:
            driver.find_element(By.ID, "submit").click() # on clique sur l'élément

        try:
            elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "passwordInput")) # on cherche l'élément par son id
            )
        finally:
            driver.find_element(By.ID, "passwordInput").send_keys(password) # on entre le mot de passe dans l'élément

        try:
            elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "submitButton")) # on cherche l'élément par son id
            )
        finally:
            driver.find_element(By.ID, "submitButton").click() # on clique sur l'élément

        global_exam_connection() # on relance la fonction

    else: # si l'url actuel n'est ni l'url de l'ENT ni l'url de connection à l'ENT
        print(driver.current_url) # on affiche l'url actuel



def do_exercice(): # Faire les exercices
    # On crée une boucle qui fera le nombre d'exercice demandé par l'utilisateur (nbr_exercice)
    for i in range(int(nbr_exercice)): 
        driver.get(correspondance_type_nbr[int(type_exercice)][1]) # on ouvre l'url correspondant au type d'exercice
        time.sleep(1)

        try:
            elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//label[@class='form-checkbox flex items-center']")) # on cherche l'élément par son xpath
            )
        finally:
            checkbox_elements = driver.find_elements(By.XPATH, "//label[@class='form-checkbox flex items-center']")  # on cherche l'élément par son xpath
            for checkbox_element in checkbox_elements:
                if i==1:
                    checkbox_element.click() # on coche la checkbox
                    time.sleep(1)

        select_lvl = Select(driver.find_element(By.XPATH, "//select[@class='h-8 px-4 appearance-none bg-background border border-solid border-neutral-10 w-full leading-snug rounded-size-24 cursor-pointer lg:pl-5 lg:py-3 lg:pr-8 lg:h-auto']")) # on cherche l'élément par son xpath
        select_lvl.select_by_visible_text(lvl)
        try:
            elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Test myself')]")) # on cherche l'élément par son xpath
            )
        except:
            print("\n\n\nTous les exercices de cette catégorie et de ce niveau ont été complétés")
            return
        else:
            button = driver.find_element(By.XPATH, '//button[contains(., "Test myself")]') # on cherche l'élément par son xpath
            button.click()
            time.sleep(1)
        
        
        exercice = "Answer the following exercise, each time noting down the 10 answers (you need 10 answers!!) (only the part you've completed) without anything else (especially not \"answer 1:\" before the answer), separated by a |.\n" # on crée la variable exercice qui contiendra le prompt

        try:
            elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'wysiwyg ch-bg-selection text-neutral-80 break-words')]")) # on cherche l'élément par son xpath
            )
        finally:
            enonce_element = driver.find_element(By.XPATH, "//div[contains(@class, 'wysiwyg ch-bg-selection text-neutral-80 break-words')]") # on cherche l'élément par son xpath
        
        exercice += enonce_element.text + "\n" # on ajoute le texte de l'élément à la variable exercice
        question_elements = driver.find_elements(By.XPATH,'//div[@class="card px-4 py-8 lg:px-8 lg:py-6"]//div/p[@class="text-neutral-80 leading-tight mb-8"]') # on cherche l'élément par son xpath

        for question_element in question_elements: 
            question_text = question_element.text # on stocke le texte de l'élément
            exercice +=  question_text + "\n" # on ajoute le texte de l'élément à la variable exercice


        print("Prompt envoyé à OpenAI :")
        print(exercice)
        completion = openai.Completion.create(engine="text-davinci-003", prompt=exercice, max_tokens=1000,temperature=0.25)
        print("Réponse de OpenAI :")
        print(completion.choices[0]['text'])
        response_list = completion.choices[0]['text'].split("|")

        # Vérifiez si response_list a moins de 10 réponses
        if len(response_list) < 10:
            # Si response_list a moins de 10 réponses, ajoutez des réponses vides pour atteindre 10 réponses
            while len(response_list) < 10:
                response_list.append("")

        # Si response_list a plus de 10 réponses, retirez les réponses supplémentaires
        if len(response_list) > 10:
            response_list = response_list[:10]

        input_elements = driver.find_elements(By.XPATH, "//input[@type='text']")

        # on complète l'exercice en respectant le temps donné par l'utilisateur
        waiting_time = int(temps)/len(input_elements)
        for i in range(len(input_elements)):
            time.sleep(waiting_time)
            input_element = input_elements[i]
            response_word = response_list[i]
            # Utilisez 'send_keys' pour insérer le mot dans le champ d'entrée
            input_element.send_keys(response_word)

        time.sleep(1)

        # Localisez le bouton "Validate" par son texte (ou d'une autre manière si nécessaire)
        validate_button = driver.find_element(By.XPATH, "//button[contains(., 'Validate')]")

        # Cliquez sur le bouton "Validate"
        validate_button.click()
        time.sleep(2)
        if correspondance_lire_fiche[int(lire_fiche)][1] == True:
            try:
                elem = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Read the study sheet')]")) # on cherche l'élément par son xpath
                )
            finally:
                button = driver.find_element(By.XPATH, "//a[contains(., 'Read the study sheet')]") # on cherche l'élément par son xpath
                button.click()
                time.sleep(1)
                # on scroll jusqu'en bas de la fiche
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

menu()

