"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install -e .`
- Use the same interpreter as the one used to install the bot (`pip install -e .`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""

from pathlib import Path
from botcity.web.browsers.chrome import default_options
from botcity.web import WebBot, Browser
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import glob
import os.path
import csv

# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *


class Bot(WebBot):
    def action(self, execution=None):
        # Uncomment to silence Maestro errors when disconnected
        # if self.maestro:
        #     self.maestro.RAISE_NOT_CONNECTED = False
        PASTA_RAIZ = str(Path(__file__).parent.parent)
        # Configure whether or not to run on headless mode
        self.headless = False

        # Uncomment to change the default Browser to Firefox
        self.browser = Browser.CHROME

        # Uncomment to set the WebDriver path
        self.driver_path = ChromeDriverManager().install()

        var_pastaDownload = PASTA_RAIZ + r'\Planilha' 
        print(var_pastaDownload)

        self.options = default_options(download_folder_path=var_pastaDownload)

        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        # Opens the BotCity website.
        self.browse("https://pathfinder.automationanywhere.com/challenges/automationanywherelabs-customeronboarding.html")
        self.maximize_window()
        
        #Click em 'aceitar cookies'
        var_inputCookie = self.find_element(selector='//button[@id="onetrust-accept-btn-handler"]', by='xpath')
        var_inputCookie.click()

        #Click em 'login'
        var_btnCommunityLogin = self.find_element(selector='//button[@id="button_modal-login-btn__iPh6x"]', by='xpath')
        var_btnCommunityLogin.click()
        
        #Insira o 'Email'
        var_inputEmail = self.find_element(selector='//input[@id="42:2;a"]', by='xpath')
        var_inputEmail.send_keys('t41957070@gmail.com')
        
        #Click em 'Next'
        var_btnNext = self.find_element(selector='//button[@class="slds-button slds-button_brand button"]', by='xpath')
        var_btnNext.click()

        #Inseria a 'Senha'
        var_inputSenha = self.find_element(selector='//input[@class="textbox input sfdc_passwordinput sfdc input"]', by='xpath')
        var_inputSenha.send_keys('XAqcRuFbeIfZ2T1')
        
        #Click em 'Log in'
        var_btnLogin = self.find_element(selector='//button[@class="slds-button slds-button_brand button"]', by='xpath')
        var_btnLogin.click()

        #Click em 'Download CSV'
        var_btnDownload = self.find_element(selector='//a[@class="btn customer-onboarding__btn-orange"]', by='xpath')
        var_btnDownload.click()

        self.wait(3000)

        var_TipoArquivo = r'\*csv'
        var_Arquivo = glob.glob(var_pastaDownload + var_TipoArquivo)
        var_UltimoArquivo = max(var_Arquivo,key=os.path.getctime)

        with open(var_UltimoArquivo, 'r') as var_arquivoCSV:

            var_LeitorCSV = csv.reader(var_arquivoCSV)
            
            next(var_LeitorCSV)

            for dados in var_LeitorCSV:
          
                var_strCustomerName = dados[0]
                var_strCustomerID = dados[1]
                var_strPrimaryContact = dados[2]
                var_strStreetAddress = dados[3]
                var_strCity = dados[4]
                var_strState = dados[5]
                var_strZip = dados[6]
                var_strEmail = dados[7]
                var_strDiscount = dados[8]
                var_strDisclosure = dados[9]


                var_inputCustomerName = self.find_element(selector='//input[@id="customerName"]', by='xpath')
                var_inputCustomerName.send_keys(var_strCustomerName)

                var_inputCustomerID = self.find_element(selector='//input[@id="customerID"]', by='xpath')
                var_inputCustomerID.send_keys(var_strCustomerID)

                var_inputPrimaryContact = self.find_element(selector='//input[@id="primaryContact"]', by='xpath')
                var_inputPrimaryContact.send_keys(var_strPrimaryContact)

                var_inputStreetAddress = self.find_element(selector='//input[@id="street"]', by='xpath')
                var_inputStreetAddress.send_keys(var_strStreetAddress)

                var_inputCity = self.find_element(selector='//input[@id="city"]', by='xpath')
                var_inputCity.send_keys(var_strCity)

                var_selectState = self.find_element(selector='//select[@id="state"]', by='xpath')
                var_selectState.send_keys(var_strState)

                var_inputZip = self.find_element(selector='//input[@id="zip"]', by='xpath')
                var_inputZip.send_keys(var_strZip)

                var_inputEmail = self.find_element(selector='//input[@id="email"]', by='xpath')
                var_inputEmail.send_keys(var_strEmail)
            
                if var_strDiscount == 'YES':
                    var_inputDiscountYes = self.find_element(selector='//input[@id="activeDiscountYes"]', by='xpath')
                    var_inputDiscountYes.click()

                else:
                   var_inputDiscountNo = self.find_element(selector='//input[@id="activeDiscountNo"]', by='xpath')
                   var_inputDiscountNo.click()

                if var_strDisclosure == 'YES':
                   var_inputDisclosure = self.find_element(selector='//input[@id="NDA"]', by='xpath')
                   var_inputDisclosure.click()
                
                var_btnSubmit = self.find_element(selector='//button[@id="submit_button"]', by='xpath')
                var_btnSubmit.click()

        
            self.wait(8000)
            var_Print = (var_UltimoArquivo.replace('.csv','') + '_' + datetime.now().strftime('%d-%m-%Y_%H%M%S' + '.png'))
            self.screenshot(var_Print)





        # Uncomment to mark this task as finished on BotMaestro
        # self.maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )

        # Wait for 10 seconds before closing
        self.wait(10000)

        # Stop the browser and clean up
        self.stop_browser()

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()
