import sys

from selenium import webdriver


class CoronaStats():
    def __init__(self, country, website):
        self.driver = webdriver.Chrome('<DRIVER PATH>')
        self.country = country
        self.website = website

    # If not data available for an attribute then return 0 else int value
    @staticmethod
    def check_none(value):
        if value == '':
            return '0'
        else:
            return value

    # Reading data where it found the country name
    def scrapping_data(self, table):
        # Get number of rows
        country_element = table.find_element_by_xpath("//td[contains(., '{}')]".format(self.country))
        row = country_element.find_element_by_xpath("./..")
        data = row.text.split(" ")

        return data

    def get_data(self):
        try:
            self.driver.get(self.website)
            table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
            data = self.scrapping_data(table)

            total_cases = CoronaStats.check_none(data[1])
            new_cases = CoronaStats.check_none(data[2])
            total_deaths = CoronaStats.check_none(data[3])
            total_recovered = CoronaStats.check_none(data[5])
            active_cases = CoronaStats.check_none(data[6])
            serious_critical = CoronaStats.check_none(data[7])

            self.driver.close()
            return total_cases, new_cases, total_deaths, active_cases, total_recovered, serious_critical
        except Exception as e:
            print(e)
            self.driver.quit()
            sys.exit()
