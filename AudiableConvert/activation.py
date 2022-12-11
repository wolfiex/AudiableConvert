'''
Functions for obtaining a users activation code should it not already have been provided. 

'''

# mostly headless browser based imports

import requests, re, js2py, time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException



def get_activation(checksum, url = 'https://audible-converter.ml/'):
    '''
    A function to spawn a headless browser and obtain the users activation bytes'''
    
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    print('Obtaining activation key from ', url+checksum)
    driver.get(url+checksum)

    # Wait for the page to load. Implicit/Explecit Selenium waits were not sufficient. 
    time.sleep(10)

    ab = driver.find_element(By.ID,'activationBytes')
    # make a copy of the activation bytes
    activationBytes =  ab.get_attribute('value')
    print('Your Activation Key is:',activationBytes,ab)

    # we are now done with the driver and can close it
    driver.close()

    return activationBytes




def get_key(file):
    ''' 
    A function to get the relevant checksum for Audiable
    '''
    # uint8Array
    filebuffer = open(file,'rb').read()[653: 653 + 20] 

    # a javascript function to get the checksum
    get_cs = '''
    function (bf) { 
        const buffer = new Uint8Array(bf)

        return Array.prototype.map.call(buffer, function (x) {
            return ('00' + x.toString(16)).slice(-2)}
        ).join('');  
        }'''

    get_cs_fn = js2py.eval_js(get_cs)
    checksum = get_cs_fn(list(filebuffer))

    assert re.match('[a-f0-9]{40}', checksum)

    return get_activation(checksum)








# Notes.


    # Coutesy of audible-tools.github.io
    # res = requests.get("https://api.audible-converter.ml/api/v2/activation/" + 
    # checksum).json()
    # print(res)

    # return res['activationBytes']

    # '''        { format: "m4b", codec: ["-c","copy"] },
    #     { format: "flac", codec: ["-c:a","flac"] },
    #     { format: "mp3", codec: ["-c:a","libmp3lame"] },
    #     '7d757703'
    #     '''
