# Code from url: https://kgptalkie.com/linkedin-auto-connect-bot-with-personalized-messaging/

import os, random, sys, time
#from urlib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome(executable_path=r'C:\Users\bruno\OneDrive\Documentos\webdriver-chrome/chromedriver.exe')
browser.get('https://www.linkedin.com/login')

# file = open('config.txt')
#lines = file.readlines()
#username = lines[0]
#password = lines[1]
username = "xxxxxxxxxxx"
password = "xxxxxxxxxxx"

elementID = browser.find_element_by_id('username')
elementID.send_keys(username)
time.sleep(random.uniform(3, 7))

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
time.sleep(random.uniform(3, 7))

elementID.submit()
time.sleep(random.uniform(3, 7))

visitingProfileID = 'in/brunoafabricio'
fullLink = 'https://linkedin.com/' + visitingProfileID
browser.get(fullLink)

visitedProfiles = []
profilesQueued = []

def getNewProfileIDs(soup, profilesQueued):
    profilesID = []
    pav = soup.find('div', {'class': 'pv-browsemap-section'})
    all_links = pav.findAll('a', {'class': 'pv-browsemap-section__member'})
    for link in all_links:
        userID = link.get('href')
        if((userID not in profilesQueued) and (userID not in visitedProfiles)):
            profilesID.append(userID)
    return profilesID

getNewProfileIDs(BeautifulSoup(browser.page_source), profilesQueued)


profilesQueued = getNewProfileIDs(BeautifulSoup(browser.page_source), profilesQueued)

while profilesQueued:
    try:
        visitingProfileID = profilesQueued.pop()
        visitedProfiles.append(visitingProfileID)
        fullLink = 'https://www.linkedin.com' + visitingProfileID
        browser.get(fullLink)

        browser.find_element_by_class_name('pv-s-profile-actions').click()

        browser.find_element_by_class_name('mr1').click()

        customMessage = "Olá, tudo bem? Sou novo por aqui e estou procurando fazer novas conexões. Gostei do teu perfil, posso te adicionar? "
        elementID = browser.find_element_by_id('custom-message')
        elementID.send_keys(customMessage)

        browser.find_element_by_class_name('ml1').click()

        # Add the ID to the visitedUsersFile
        with open('visitedUsers.txt', 'a') as visitedUsersFile:
            visitedUsersFile.write(str(visitingProfileID)+'\n')
        visitedUsersFile.close()

        # Get new profiles ID
        soup = BeautifulSoup(browser.page_source)
        try: 
            profilesQueued.extend(getNewProfileIDs(soup, profilesQueued))
        except:
            print('Continue')

        # Pause
        time.sleep(random.uniform(3, 7)) # Otherwise, sleep to make sure everything loads

        if(len(visitedProfiles)%50==0):
            print('Visited Profiles: ', len(visitedProfiles))

        if(len(profilesQueued)>100):
            with open('profilesQueued.txt', 'a') as visitedUsersFile:
                visitedUsersFile.write(str(visitingProfileID)+'\n')
            visitedUsersFile.close()
            print('100 Done!!!')
            break;
    except:
        print('error')