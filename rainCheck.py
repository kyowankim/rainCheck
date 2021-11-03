import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



#Method to parse through the "Probability" elements and the child and only obtain the integers which represent the probability 
def findProbability(array):
    result = []
    for sentence in array:
        for index,value in enumerate(sentence.text):
            if value.isdigit():
                end = index+1
                while(sentence.text[end].isdigit()):
                    end += 1
                result.append(int(sentence.text[index:end]))
                break
    return result

#Method to parse through the "Inches Of Precipitation" elements and it's child to get decimal points
def findInches(array):
    result = []
    for sentence in array:
        for index,value in enumerate(sentence.text):
            if value.isdigit():
                end = index+1
                while(sentence.text[end] != ' '):
                    end += 1
                result.append(sentence.text[index:end])
                break
    return result

def sendText(arrProbOfPrecip,arrProbOfThunder,inchesOfPrecip,date):
    if arrProbOfPrecip[0] or arrProbOfPrecip[1] >= 50:
        message = "You might need an umbrella today!"
    if arrProbOfThunder[0] or arrProbOfThunder[1] >= 50:
        message = "**UMBRELLA MIGHT BE NEEDED**"
    else:
        message = "No umbrella is needed today"

    linebreak = "\n--------------------------\n"
    probabilityOfPrecipitation = f"Day: {arrProbOfPrecip[0]}%  |  Night: {arrProbOfPrecip[1]}%"
    probabilityOfThunderStorm = f"Day: {arrProbOfThunder[0]}%  |  Night: {arrProbOfThunder[1]}%"
    inchesOfPrecipitation = f'Day: {inchesOfPrecip[0]}"  |  Night: {inchesOfPrecip[1]}"  '

    body = f"\n      {date}\n\nProbability of Precipitation \n{probabilityOfPrecipitation}\
                    {linebreak}Probability of Thunderstorm\n{probabilityOfThunderStorm}\
                    {linebreak}Inches Of Precipitation\n{inchesOfPrecipitation}"

    email = "kyobiwankim@gmail.com"
    pas = "zpeduvtrzjkpwqoq"
    sms_gateway = '9087647244@tmomail.net'
    # The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
    # and port is also provided by the email provider.
    smtp = "smtp.gmail.com" 
    port = 587
    # This will start our email server
    server = smtplib.SMTP(smtp,port)
    # Starting the server
    server.starttls()
    # Now we need to login
    server.login(email,pas)

    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    # Make sure you add a new line in the subject
    msg['Subject'] = f"{message}\n"

    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    server.sendmail(email,sms_gateway,sms)

    # lastly quit the server
    server.quit()

def main():
    class My_Chrome(uc.Chrome):
        def __del__(self):
            pass
    options = uc.ChromeOptions()
    # options.headless = True
    driver = My_Chrome(executable_path="C:\\Program Files\\Python39\\Scripts\\chromedriver.exe",options=options)
    # driver.get("https://www.accuweather.com/en/us/boston/02108/daily-weather-forecast/348735?day=2")


    driver.get("https://www.accuweather.com/en/us/boston/02108/daily-weather-forecast/348735?day=18")
    driver.implicitly_wait(1)
    probOfPrecip = driver.find_elements(By.XPATH, "//p[text()='Probability of Precipitation']")
    probOfThunder = driver.find_elements(By.XPATH, "//p[text()='Probability of Thunderstorms']")
    inchesOfPrecip = driver.find_elements(By.XPATH, "//p[text()='Precipitation']")
    # Double for loop to find only the integers
    arrProbOfPrecip = findProbability(probOfPrecip)
    arrProbOfThunder = findProbability(probOfThunder)
    inchesOfPrecip = findInches(inchesOfPrecip)
    date = driver.find_element(By.XPATH, "//div[@class='subnav-pagination']").text
    sendText(arrProbOfPrecip,arrProbOfThunder,inchesOfPrecip,date)

if __name__=="__main__":
    main()
