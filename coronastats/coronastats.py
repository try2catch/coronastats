import sys

from selenium import webdriver


class CoronaStats:
    def __init__(self, country, website):
        self.driver = webdriver.Chrome('/Users/akhileshsingh/Desktop/Drivers/chromedriver')
        self.country = country
        self.website = website

    def get_row_count(self, table):
        return len(table.find_elements_by_tag_name('tr')) - 1

    def get_columns_count(self, table):
        return len(table.find_elements_by_xpath('//tr[2]/td'))

    def check_none(self, value):
        if value == '':
            return 0
        else:
            return int(value)

    def scrapping_data(self, table):

        noOfRows = self.get_row_count(table)
        noOfColumns = self.get_columns_count(table)

        allData = []
        for i in range(1, noOfRows):
            found_country = table.find_element_by_xpath("//tr[" + str(i) + "]/td[1]").text

            if found_country == self.country:
                for j in range(1, noOfColumns):
                    allData.append(table.find_element_by_xpath("//tr[" + str(i) + "]/td[" + str(j) + "]").text)

                break
        return allData

    def get_data(self):
        try:
            self.driver.get(self.website)
            table = self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/tbody[1]')
            data = self.scrapping_data(table)

            total_cases = self.check_none(data[1])
            new_cases = self.check_none(data[2])
            total_deaths = self.check_none(data[3])
            new_deaths = self.check_none(data[4])
            total_recovered = self.check_none(data[5])
            active_cases = self.check_none(data[6])
            serious_critical = self.check_none(data[7])

            self.driver.close()
            return total_cases, new_cases, total_deaths, active_cases, total_recovered, serious_critical
        except Exception as e:
            print(e)
            self.driver.quit()
            sys.exit()
