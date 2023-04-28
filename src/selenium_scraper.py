from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

import numpy as np


def get_travel_time(coord1, coord2):
    """
    Calculate travel time using public transport between two coordinates via Google Maps.

    Args:
        coord1 (str): x and y coordinates (latitude and longitude) in CRS 4326 of origin.
        coord2 (str): x and y coordinates (latitude and longitude) in CRS 4326 of destination.

    Returns:
        float: Travel time in minutes.

    Example:
        origin = "51.535733, -0.123565"
        destination = "51.5130377,-0.1129969"
        travel_time = get_travel_time(origin, destination)
    """
    driver = webdriver.Chrome()  # Use the appropriate WebDriver for your browser
    driver.get("https://www.google.com/maps")
    
    time.sleep(2)
    driver.find_element("xpath", """//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button""").click() #click on accept all for cookies t&cs
    
    time.sleep(2)
    
    # Click on the Directions button
    directions_button = driver.find_element("xpath", """//*[@id="hArJGc"]""")
    directions_button.click()
    time.sleep(2)
    
    

    # Enter the origin and destination coordinates
    origin_input = driver.find_element("xpath", """//*[@id="sb_ifc51"]/input""")
    origin_input.clear() #clear existing field
    origin_input.send_keys(f"{coord1}")
    origin_input.send_keys(Keys.ENTER)


    destination_input = driver.find_element("xpath", """//*[@id="sb_ifc52"]/input""")
    destination_input.send_keys(f"{coord2}")
    destination_input.send_keys(Keys.ENTER)


    # Select public transport mode
    transit_button = driver.find_element("xpath", """//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[3]/button/img""")
    transit_button.click()
    time.sleep(2)

    # Get travel time
    # Sometimes No public transport route available therefore, script waits 10 seconds for route to be calculated otherwise times out and na is returned.

    try:
        # Get travel time
        travel_time_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[3]/button/div[1]""")))

        travel_time = travel_time_element.text
    except TimeoutException:
        print("Travel time element not found within 10 seconds")
        travel_time=np.nan
    
  
    
    driver.quit()
    return travel_time