import os
import re
import patoolib

import urllib.request
import requests

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time


    # URL of the .gz file without the code sample
urlFirstHalf = r'https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.'
urlSecondHalf = r'.sampleMap%2FHiSeqV2_PANCAN.gz'

    # URL of the hub
mainURL = 'https://xenabrowser.net/datapages/?hub=https://tcga.xenahubs.net:443'

    #Path of chromedrivers for windows and linux
windows64 = r'\chromedriver-win64\chromedriver.exe'
linux64 = r'\chromedriver-linux64\chromedriver'

    # Get the directory where you download the items from OS 
filePath = os.path.dirname(__file__)

    #HTTP GET request response 
r = requests.get(mainURL)


# Step 1: Set up the WebDriver (e.g., for Chrome)
services = Service(filePath + windows64 )  # Replace with the actual path to ChromeDriver, do linux64 if you are on linux operating system
driver = webdriver.Chrome(service=services)

# Step 2: Open the webpage
driver.get(mainURL)

#Wait for a few seconds to allow JavaScript to load the content
time.sleep(5)

# Step 3: Extract the text
page_text = driver.find_element(By.TAG_NAME, "ul").text

# Step 4: Close the browser
driver.quit()


# Regular expression to find codes in parentheses
codes = re.findall(r'\((\w+)\)', page_text)

# Loop through the list and print each item
for code in codes:
        #final path where items will be downloaded
    output_path = filePath + r'\DownloadedItems\TCGA.' + code + '.SampleMapHiSeqV2_PANCAN.gz'

        #combining the url into a working download link
    url = urlFirstHalf + code + urlSecondHalf

    try:
            # Print the starting download information
        print(f"Starting download of {code}...")
        
              # Download the file from urllib, module request
        urllib.request.urlretrieve(url, output_path)


        
            #this is the path to .gz files without the actual file in the path
        actualFilePathOfDownloadedFiles = filePath + '\\DownloadedItems\\'

        os.chdir(actualFilePathOfDownloadedFiles)

        item = 'TCGA.' + code + '.SampleMapHiSeqV2_PANCAN'

        patoolib.extract_archive(item + '.gz', outdir=item)

        #print(f"Downloaded: {output_path}")
        
            # After downloading, check if the file exists to confirm it's completed
        if os.path.exists(output_path):
            print(f"Downloaded {code} successfully to {output_path}\n")
        else:
            print(f"Failed to download {code}. File not found after download.\n")
    
    except urllib.error.HTTPError as e:
            # This will catch HTTP-specific errors like 404, 500, etc.
        print(f"HTTP error occurred while downloading {code}: {e}")
    
    except urllib.error.URLError as e:
            # This will catch errors related to network issues (e.g., no connection, wrong URL)
        print(f"Network error occurred while downloading {code}: {e}")
    
    except PermissionError as e:
            # This will catch issues with writing to the disk (e.g., file permission issues)
        print(f"Permission error occurred while downloading {code}: {e}")
    
    except Exception as e:
            # This will catch any other unexpected errors
        print(f"An error occurred while downloading {code}: {e}")

  
    os.remove(output_path)