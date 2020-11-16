import os
import time
import requests
import schedule
import math
from discord import Webhook, RequestsWebhookAdapter, File

# create environmental variable and store it
WEBHOOKCODE = os.getenv('WEBHOOK')
WEBHOOKTOKEN = os.getenv('WEBHOOK_TOKEN')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
WEATHERAPI = os.getenv('WEATHERAPI')
webhook = Webhook.partial(
   int(WEBHOOKCODE) , WEBHOOKTOKEN,
    adapter=RequestsWebhookAdapter())

# request api
resp = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&exclude=minutely,daily&units=metric&appid={WEATHERAPI}")


# responses for requests
oneForecastDescription = resp.json()['hourly'][1]['weather'][0]['description']
currentWeather = resp.json()['hourly'][0]['weather'][0]['description']
OneHourForecastTime = resp.json()['hourly'][1]['dt']
currentTemp = math.ceil(resp.json()['hourly'][1]['temp'])
hourly = resp.json()['hourly']
airPressure = resp.json()['hourly'][1]['pressure']
    
# forecastTimeNormal = datetime.datetime.fromtimestamp(
#     int(OneHourForecastTime)).strftime('%H:%M')
# conditionals for emoji(cloud or clear)
if 'cloud' in currentWeather:
    emoji = '\U00002601'

if 'clear' in currentWeather:
    emoji = '\U00002600'
    
if 'rain' in currentWeather:
    emoji = '\U00002614'

if 'rain' in oneForecastDescription:
    rainAmount = resp.json()['hourly'][1]['rain']['1h']

# headache if air pressure drops
# source :
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4684554/
# standard atmoshperic pressure in hPa = 1013
def ifHeadache():
    if airPressure < 1013:
        webhook.send('Low air pressure\n' + 'Your head may hurt')
    elif airPressure > 1013:
        webhook.send('High air pressure, your head will not hurt for sure')
    elif airPressure < 1000:
        webhook.send('Very low air pressure \n'+'Your head will definitely hurt')
    else:
       webhook.send('Normal air pressure, your head will likely not hurt')

def currentWeatherInfo():
     webhook.send('The current weather is:\n' + currentWeather+ emoji+' and ' + str(currentTemp) + '°C')
            
# main function to send for rain forecasts through webhook
def ifRainInNextHour():
    if oneForecastDescription == 'light rain':
        webhook.send('Light rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'moderate rain':
        webhook.send('Moderate rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'heavy intensity rain':
        webhook.send('High intensity rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'very heavy rain':
        webhook.send('Very heavy rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'extreme rain':
        webhook.send('Extreme rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'freezing rain':
        webhook.send('Freezing rain\U00002614 in the next hour'  + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'light intensity shower rain':
        webhook.send('Light intensity shower rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'shower rain':
        webhook.send('Shower rain in the next hour with\n' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'heavy intensity shower rain':
        webhook.send('Heavy intensity shower rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    elif oneForecastDescription == 'ragged rain':
        webhook.send('Ragged rain \U00002614 in the next hour' + '\n with ' +
                     str(rainAmount) + ' mm of rain')
    else:
        webhook.send('Yay! No rain in the next hour')
        currentWeatherInfo()
        
        
        


    
ifRainInNextHour()
ifHeadache()
    
# run program and then every hour, and every day at 7.30


schedule.every().hour.do(ifRainInNextHour)
schedule.every().hour.do(ifHeadache)
schedule.every().day.at("07:30").do(ifHeadache)
schedule.every().day.at("07:30").do(ifRainInNextHour)


# run loop forever
while True:
        schedule.run_pending()
        time.sleep(1)


