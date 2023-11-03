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


load_dotenv()
openai.api_key = os.environ.get("openai_api_key")
login=os.environ.get("ent_cesi_login")
password=os.environ.get("ent_cesi_password")
nbr_exercice = 0

def menu():
    nombre_exercice()

def nombre_exercice():
    print('Nombre d\'exercice à compléter (entre 1 et 100):')
    nbr_exercice = input()
    # si l'entré n'est pas un nombre ou ne répond pas au condition on relance le menu
    if nbr_exercice.isnumeric() == False:
        print('Veuillez entrer un nombre entre 1 et 100')
        nombre_exercice()
    elif int(nbr_exercice) < 1 or int(nbr_exercice) > 100:
        print('Veuillez entrer un nombre entre 1 et 100')
        nombre_exercice()

def launch_chrome():
    # Spécifiez le chemin vers le pilote du navigateur Chrome WebDriver
    service = Service(executable_path='./chromedriver/chromedriver.exe')
    options = Options()
    options.add_argument("--start-maximized")
    options.page_load_strategy = 'eager'
    global mainWindow
    mainWindow = None
    # Créez une instance du navigateur Chrome
    global driver
    driver = webdriver.Chrome(service=service, options=options)

def global_exam_connection():

    url = 'https://ent.cesi.fr/accueil-apprenant'
    driver.get(url)

    if driver.current_url == "https://ent.cesi.fr/accueil-apprenant":

        driver.get("https://moodle.cesi.fr/login/index.php?authCAS=CAS")
        driver.get("https://moodle.cesi.fr/course/view.php?id=3337")

        mainWindow = driver.current_window_handle
        driver.get("https://moodle.cesi.fr/mod/lti/view.php?id=58498")

        handles = driver.window_handles
        for handle in handles:
            if handle != mainWindow:
                driver.switch_to.window(handle)

        driver.get("https://general.global-exam.com/")
        # on appui sur le bouton de type "button" contenant "General English"
        time.sleep(1)
        button = driver.find_element(By.XPATH, "//button[span[contains(., 'General English')]]").click()
        time.sleep(1)

    elif driver.current_url == "https://wayf.cesi.fr/login?service=https%3A%2F%2Fent.cesi.fr%2Fservlet%2Fcom.jsbsoft.jtf.core.SG%3FPROC%3DIDENTIFICATION_FRONT":

        driver.find_element(By.ID, "login").send_keys(login)
        driver.find_element(By.ID, "submit").click()
        driver.find_element(By.ID, "passwordInput").send_keys(password)
        driver.find_element(By.ID, "submitButton").click()
        global_exam_connection()

    else:

        print(driver.current_url)



def do_exercice():
    # On crée une boucle qui fera le nombre d'exercice demandé par l'utilisateur (nbr_exercice)
    for i in range(int(nbr_exercice)):
        driver.get("https://general.global-exam.com/library/study-sheets/categories/grammar")
        time.sleep(1)
        checkbox_element = driver.find_element(By.XPATH, "//label[contains(text(), 'Not tested only')]/input")
        checkbox_element.click()
        time.sleep(1)
        button = driver.find_element(By.XPATH, '//button[contains(., "Test myself")]')
        
        button.click()
        time.sleep(1)

        exercice = "Answer the following exercise, noting each answer (only the part you have completed) without anything else (especially no Answer 1:), separated by a |.\n"
        #récuperer le contenu de l'élement avec les classes suivante : 
        enonce_element = driver.find_element(By.XPATH, "//div[contains(@class, 'wysiwyg ch-bg-selection text-neutral-80 break-words')]")
        exercice += enonce_element.text + "\n"
        question_elements = driver.find_elements(By.XPATH,'//div[@class="card px-4 py-8 lg:px-8 lg:py-6"]//div/p[@class="text-neutral-80 leading-tight mb-8"]')

        i = 0
        for question_element in question_elements:
            i+=1
            question_text = question_element.text
            exercice +=  question_text + "\n"

        print(exercice)
        completion = openai.Completion.create(engine="text-davinci-003", prompt=exercice, max_tokens=1000)
        print(completion.choices[0]['text'])
        response_list = completion.choices[0]['text'].split("|")

        input_elements = driver.find_elements(By.XPATH, "//input[@type='text']")

        for i in range(len(input_elements)):
            # Assurez-vous que la liste 'input_elements' a le même nombre d'éléments que la liste 'response_list'
            input_element = input_elements[i]
            response_word = response_list[i]
            # Utilisez 'send_keys' pour insérer le mot dans le champ d'entrée
            print (response_word)
            input_element.send_keys(response_word)

        print('réponse envoyée')
        time.sleep(1)

        # Localisez le bouton "Validate" par son texte (ou d'une autre manière si nécessaire)
        validate_button = driver.find_element(By.XPATH, "//button[contains(., 'Validate')]")

        # Cliquez sur le bouton "Validate"
        validate_button.click()

menu()

launch_chrome()

global_exam_connection()

print('fini')
time.sleep(15)

driver.quit()

