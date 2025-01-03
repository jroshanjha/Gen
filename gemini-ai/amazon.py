import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # Uncomment below line to run Chrome in headless mode
    chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_amazon_products(search_term, num_products=5):
    driver = setup_chrome_driver()
    products = []
    try:
        url_list = [
            "https://www.amazon.com",
            "https://www.ebay.com",
            "https://www.walmart.com",
            "https://www.target.com",
            "https://www.flipkart.com/",
            "https://www.myntra.com/",
            "https://www.snapdeal.com",
            "https://www.zeptonow.com/",
        ]
        
        
            # "https://www.aliexpress.com",
            # "https://www.newegg.com",
            # "https://www.rakuten.com",
    
        # Randomly select a URL
        random_url = random.choice(url_list)
    
        # Navigate to Amazon
        driver.get("https://www.amazon.com")
        #driver.get(random_url)
        
        # Find and fill search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(search_term)
        search_box.submit()
        
        # Wait for results
        time.sleep(2)
        
        # Get product details
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-component-type='s-search-result']")
            )
        )
        
        for element in product_elements[:num_products]:
            try:
                title = element.find_element(By.XPATH, ".//h2//span").text
                try:
                    price = element.find_element(
                        By.XPATH, ".//span[@class='a-price-whole']"
                    ).text
                except:
                    price = "N/A"
                    
                try:
                    rating = element.find_element(
                        By.XPATH, ".//span[@class='a-icon-alt']"
                    ).text
                except:
                    rating = "No rating"
                
                products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating
                })
            except:
                continue
                
    finally:
        driver.quit()
        
    return pd.DataFrame(products)

def main():
    st.title("Amazon Product Scraper")
    
    # User inputs
    search_term = st.text_input("Enter product to search:")
    num_products = st.number_input("Number of products to scrape:", 
                                 min_value=1, max_value=20, value=5)
    
    if st.button("Start Scraping"):
        if search_term:
            with st.spinner("Scraping products..."):
                try:
                    df = scrape_amazon_products(search_term, num_products)
                    
                    # Display results
                    st.success("Scraping completed!")
                    st.subheader("Results:")
                    st.dataframe(df)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name="amazon_products.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a search term")

if __name__ == "__main__":
    main()