from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
import time

#list of cities to scrape; can be expanded
cities = [
    'nyc', 'la', 'chicago', 'houston', 'miami', 
    'philadelphia', 'phoenix', 'sanantonio', 'sandiego', 'dallas', 
    'sanjose', 'austin', 'jacksonville', 'fortworth', 'columbus', 
    'charlotte', 'sanfrancisco', 'indianapolis', 'seattle', 'denver', 
    'washington', 'boston', 'elpaso', 'nashville', 'detroit', 'portland', 'lasvegas', 'memphis', 'louisville', 
    'baltimore', 'milwaukee', 'albuquerque', 'tucson', 'fresno', 
    'kansascity', 'mesa', 'atlanta', 
    'coloradosprings', 'virginiabeach', 'raleigh', 'omaha', 'miami',
    'oakland', 'minneapolis', 'tulsa', 'wichita', 'neworleans'
]

# Set the URL of the Facebook Marketplace automotive category
base_url = 'https://www.facebook.com/marketplace/{}/vehicles'
urls = [base_url.format(city) for city in cities]

# Create a new Selenium WebDriver instance

chrome_service = ChromeService(executable_path='C:/Users/athiyam/Downloads/chromedriver-mac-arm64')
driver = webdriver.Chrome(service=chrome_service)

# Create a list to store the scraped data
data = {}
for url in urls:
    # Navigate to the URL
    driver.get(url)
    time.sleep(2)
    scroll = 2000

    # Wait for the page to load
    time.sleep(2)

    for i in range(50):
        driver.execute_script(f"window.scrollTo(1, {scroll})")
        scroll += 1000
        time.sleep(.5)

    # Get the HTML of the page
    html = driver.page_source

    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find all of the automotive listings on the page
    listings = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')

    # Iterate over the listings and scrape the data
    for listing in listings:
        try:
            # Get the title of the listing
            title = listing.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6').text
        except AttributeError:
            title = 'N/A'  # Handle missing title
        
        try:
            # Get the price of the listing
            price = listing.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text
        except AttributeError:
            price = 'N/A'  # Handle missing price
        
        try:
            # Get the location of the listing
            location = listing.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84').text
        except AttributeError:
            location = 'N/A'  # Handle missing location
        
        try:
            # Get the miles of the car
            miles = listing.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')[1].text
        except (AttributeError, IndexError):
            miles = 'N/A'  # Handle missing miles

        try:
            # Get the link to the listing
            link = 'https://www.facebook.com' + listing.find('a', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv')['href']
        except (AttributeError, TypeError):
            link = 'N/A'  # Handle missing link
        
        # Add the data to the list
        if (title, price, location, miles, link) not in data:
            data[(title, price, location, miles, link)] = True

# Close the Selenium WebDriver instance
driver.quit()

# Create a Pandas DataFrame from the scraped data
df = pd.DataFrame(list(data.keys()), columns=['Title', 'Price', 'Location', 'Miles', 'Link'])
df.dropna(how='all', inplace=True)

# Write the DataFrame to an Excel file
df.to_excel('facebook_marketplace_automotive_postings.xlsx', index=False)