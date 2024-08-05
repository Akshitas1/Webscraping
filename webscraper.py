from bs4 import BeautifulSoup
import requests
import pandas as pd

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.page = None
        self.soup = None
        self.data = []
        self.counter = 1

    def extracting_page(self):
        self.page = requests.get(self.url) 
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def extracting_data(self, element, argm, classname=None):
        self.data = self.soup.find_all(element, class_=classname)

    def extract_table_data(self, table):
        table_titles = table.find_all('th')
        titles = [title.text.strip() for title in table_titles]
        df = pd.DataFrame(columns=titles)
        column_data = table.find_all('tr')
        for row in column_data[1:]:  
            row_data = row.find_all('td')
            individual_row_data = [data.text.strip() for data in row_data]
            df.loc[len(df)] = individual_row_data  
        return df

    def data_into_csv(self, df):
        filename = f'output_{self.counter}.csv'
        df.to_csv(filename, index=False)
        self.counter += 1

if __name__ == "__main__":  
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    scraping = WebScraper(url)
    scraping.extracting_page()
    scraping.extracting_data('table', 'class', 'wikitable')
    if scraping.data:
        df = scraping.extract_table_data(scraping.data[0])
        scraping.data_into_csv(df)
        df2 = scraping.extract_table_data(scraping.data[1])
        scraping.data_into_csv(df2)
        df3 = scraping.extract_table_data(scraping.data[2])
        scraping.data_into_csv(df3)
    else:
        print("No data found.")
