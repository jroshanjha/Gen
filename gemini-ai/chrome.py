# import streamlit as st
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time

# def setup_chrome_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     # chrome_options.add_argument("--headless")
    
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     return driver

# def scrape_website(url, search_term=None, css_selectors=None):
#     driver = setup_chrome_driver()
#     data = []
    
#     try:
#         # Navigate to the provided URL
#         driver.get(url)
#         time.sleep(2)  # Allow page to load
        
#         # If search functionality is needed
#         if search_term and css_selectors.get('search_box'):
#             try:
#                 search_box = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, css_selectors['search_box']))
#                 )
#                 search_box.send_keys(search_term)
#                 search_box.submit()
#                 time.sleep(2)
#             except Exception as e:
#                 st.warning(f"Search box not found: {str(e)}")
        
#         # Extract data based on provided selectors
#         if css_selectors:
#             items = WebDriverWait(driver, 10).until(
#                 EC.presence_of_all_elements_located(
#                     (By.CSS_SELECTOR, css_selectors['item_container'])
#                 )
#             )
            
#             for item in items[:10]:  # Limit to 10 items by default
#                 item_data = {}
#                 for key, selector in css_selectors['fields'].items():
#                     try:
#                         element = item.find_element(By.CSS_SELECTOR, selector)
#                         item_data[key] = element.text
#                     except:
#                         item_data[key] = "N/A"
#                 data.append(item_data)
                
#     except Exception as e:
#         st.error(f"Scraping error: {str(e)}")
        
#     finally:
#         driver.quit()
        
#     return pd.DataFrame(data)

# def main():
#     st.title("Universal Web Scraper")
    
#     # User inputs
#     url = st.text_input("Enter website URL to scrape:")
    
#     # Predefined selector templates
#     selector_templates = {
#         "Custom": {
#             "search_box": "",
#             "item_container": "",
#             "fields": {}
#         },
#         "Amazon": {
#             "search_box": "#twotabsearchtextbox",
#             "item_container": "div[data-component-type='s-search-result']",
#             "fields": {
#                 "Title": "h2 span",
#                 "Price": "span.a-price-whole",
#                 "Rating": "span.a-icon-alt"
#             }
#         },
#         "eBay": {
#             "search_box": "#gh-ac",
#             "item_container": ".s-item",
#             "fields": {
#                 "Title": ".s-item__title",
#                 "Price": ".s-item__price",
#                 "Status": ".s-item__subtitle"
#             }
#         }
#     }
    
#     # Template selection
#     template = st.selectbox(
#         "Select website template or custom:",
#         list(selector_templates.keys())
#     )
    
#     # Custom selectors input if needed
#     if template == "Custom":
#         st.subheader("Enter CSS Selectors")
#         search_box = st.text_input("Search box selector (optional):")
#         item_container = st.text_input("Item container selector:")
        
#         st.write("Field selectors:")
#         num_fields = st.number_input("Number of fields:", min_value=1, max_value=10, value=3)
        
#         custom_fields = {}
#         for i in range(num_fields):
#             col1, col2 = st.columns(2)
#             with col1:
#                 field_name = st.text_input(f"Field {i+1} name:")
#             with col2:
#                 field_selector = st.text_input(f"Field {i+1} selector:")
#             if field_name and field_selector:
#                 custom_fields[field_name] = field_selector
        
#         css_selectors = {
#             "search_box": search_box,
#             "item_container": item_container,
#             "fields": custom_fields
#         }
#     else:
#         css_selectors = selector_templates[template]
    
#     search_term = st.text_input("Search term (optional):")
    
#     if st.button("Start Scraping"):
#         if url:
#             with st.spinner("Scraping website..."):
#                 try:
#                     df = scrape_website(url, search_term, css_selectors)
                    
#                     if not df.empty:
#                         st.success("Scraping completed!")
#                         st.subheader("Results:")
#                         st.dataframe(df)
                        
#                         # Download button
#                         csv = df.to_csv(index=False)
#                         st.download_button(
#                             label="Download data as CSV",
#                             data=csv,
#                             file_name="scraped_data.csv",
#                             mime="text/csv"
#                         )
#                     else:
#                         st.warning("No data found with the provided selectors")
                        
#                 except Exception as e:
#                     st.error(f"An error occurred: {str(e)}")
#         else:
#             st.warning("Please enter a URL")

# if __name__ == "__main__":
#     main()



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

STORE_TEMPLATES = {
    "Amazon": {
        "url": "https://www.amazon.com",
        "search_box": "#twotabsearchtextbox",
        "item_container": "div[data-component-type='s-search-result']",
        "fields": {
            "Title": "h2 span",
            "Price": "span.a-price-whole",
            "Rating": "span.a-icon-alt"
        }
    },
    "eBay": {
        "url": "https://www.ebay.com",
        "search_box": "#gh-ac",
        "item_container": ".s-item",
        "fields": {
            "Title": ".s-item__title",
            "Price": ".s-item__price",
            "Status": ".s-item__subtitle"
        }
    },
    "Walmart": {
        "url": "https://www.walmart.com",
        "search_box": "#global-search-input",
        "item_container": "div[data-item-id]",
        "fields": {
            "Title": ".typography-product-title",
            "Price": ".price-main",
            "Rating": ".stars-container"
        }
    },
    "Target": {
        "url": "https://www.target.com",
        "search_box": "#search",
        "item_container": "li.Col-favj32-0",
        "fields": {
            "Title": "a[data-test='product-title']",
            "Price": "span[data-test='product-price']",
            "Rating": ".RatingStars"
        }
    },
    "Flipkart": {
        "url": "https://www.flipkart.com",
        "search_box": "input[name='q']",
        "item_container": "div._1AtVbE",
        "fields": {
            "Title": "div._4rR01T",
            "Price": "div._30jeq3",
            "Rating": "div._3LWZlK"
        }
    },
    "Myntra": {
        "url": "https://www.myntra.com",
        "search_box": ".desktop-searchBar",
        "item_container": "li.product-base",
        "fields": {
            "Title": ".product-brand",
            "Price": ".product-discountedPrice",
            "Rating": ".product-ratingsContainer"
        }
    },
    "Snapdeal": {
        "url": "https://www.snapdeal.com",
        "search_box": "#inputValEnter",
        "item_container": ".product-tuple-listing",
        "fields": {
            "Title": ".product-title",
            "Price": ".product-price",
            "Rating": ".product-rating"
        }
    },
    "Zepto": {
        "url": "https://www.zeptonow.com",
        "search_box": "input[type='search']",
        "item_container": ".product-item",
        "fields": {
            "Title": ".product-name",
            "Price": ".product-price",
            "Quantity": ".product-quantity"
        }
    }
}

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_multiple_stores(search_term, selected_stores):
    all_data = []
    
    for store in selected_stores:
        template = STORE_TEMPLATES[store]
        driver = setup_chrome_driver()
        
        try:
            driver.get(template["url"])
            time.sleep(random.uniform(2, 4))  # Random delay to avoid detection
            
            # Handle search
            try:
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, template["search_box"]))
                )
                search_box.clear()
                search_box.send_keys(search_term)
                search_box.submit()
                time.sleep(random.uniform(3, 5))
            except Exception as e:
                st.warning(f"Search failed for {store}: {str(e)}")
                continue
            
            # Extract data
            items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, template["item_container"])
                )
            )
            
            store_data = []
            for item in items[:5]:  # Limit to 5 items per store
                item_data = {"Store": store}
                for field, selector in template["fields"].items():
                    try:
                        element = item.find_element(By.CSS_SELECTOR, selector)
                        item_data[field] = element.text
                    except:
                        item_data[field] = "N/A"
                store_data.append(item_data)
            
            all_data.extend(store_data)
            
        except Exception as e:
            st.error(f"Error scraping {store}: {str(e)}")
            
        finally:
            driver.quit()
            time.sleep(random.uniform(1, 2))  # Delay between stores
    
    return pd.DataFrame(all_data)

def main():
    st.title("Multi-Store Product Scraper")
    
    # Store selection
    stores = list(STORE_TEMPLATES.keys())
    selected_stores = st.multiselect(
        "Select stores to scrape:",
        stores,
        default=stores[:3]
    )
    
    search_term = st.text_input("Enter product to search:")
    
    if st.button("Start Scraping"):
        if search_term and selected_stores:
            with st.spinner("Scraping products from multiple stores..."):
                df = scrape_multiple_stores(search_term, selected_stores)
                
                if not df.empty:
                    st.success("Scraping completed!")
                    
                    # Display results grouped by store
                    for store in selected_stores:
                        store_data = df[df['Store'] == store]
                        if not store_data.empty:
                            st.subheader(f"{store} Results:")
                            st.dataframe(store_data)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download all data as CSV",
                        data=csv,
                        file_name="multi_store_products.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No data found")
        else:
            st.warning("Please select stores and enter a search term")

if __name__ == "__main__":
    main()