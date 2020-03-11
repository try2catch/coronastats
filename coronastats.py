import smtplib

from selenium import webdriver


class CoronaStats():
    def __init__(self, country):
        self.driver = webdriver.Chrome()
        self.country = country

    def get_row_count(self, table):
        return len(table.find_elements_by_tag_name("tr")) - 1;

    def get_column_count(self, table):
        return len(table.find_elements_by_xpath("//tr[2]/td"));

    def get_all_data(self, table):
        # get number of rows
        noOfRows = self.get_row_count(table)
        noOfColumns = self.get_column_count(table)
        allData = []
        # iterate over the rows, to ignore the headers we have started the i with '1'
        for i in range(1, noOfRows):
            found_country = table.find_element_by_xpath("//tr[" + str(i) + "]/td[" + str(1) + "]").text
            if found_country == self.country:
                # iterate over columns
                for j in range(1, noOfColumns):
                    # get text from the i th row and j th column
                    allData.append(table.find_element_by_xpath("//tr[" + str(i) + "]/td[" + str(j) + "]").text)
                break

        return allData

    def get_data(self):
        try:
            self.driver.get('https://www.worldometers.info/coronavirus/')
            table = self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/tbody[1]')
            data = self.get_all_data(table)
            total_cases = data[1]
            new_cases = data[2]
            total_deaths = data[3]
            new_deaths = data[4]
            active_cases = data[5]
            total_recovered = data[6]
            serious_critical = data[7]

            # total_cases = row.find_element_by_class_name('sorting_1')
            # new_cases = row.find_element_by_xpath("//td[3]")
            # total_deaths = row.find_element_by_xpath("//td[4]")
            # new_deaths = row.find_element_by_xpath("//td[5]")
            # active_cases = row.find_element_by_xpath("//td[6]")
            # total_recovered = row.find_element_by_xpath("//td[7]")
            # serious_critical = row.find_element_by_xpath("//td[8]")
            print("Total cases: " + total_cases)
            print("New cases: " + new_cases)
            print("Total deaths: " + total_deaths)
            print("New deaths: " + new_deaths)
            print("Active cases: " + active_cases)
            print("Total recovered: " + total_recovered)
            print("Serious, critical cases: " + serious_critical)

            send_mail(self.country, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered,
                      serious_critical)

            self.driver.close()
        except Exception as e:
            print(e)
            self.driver.quit()


def send_mail(country_element, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered,
              serious_critical):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('rajputonnet@gmail.com', '')

    subject = 'Coronavirus stats in your country today!'

    body = 'Today in ' + country_element + '\
        \nThere is new data on coronavirus:\
        \nTotal cases: ' + total_cases + '\
        \nNew cases: ' + new_cases + '\
        \nTotal deaths: ' + total_deaths + '\
        \nNew deaths: ' + new_deaths + '\
        \nActive cases: ' + active_cases + '\
        \nTotal recovered: ' + total_recovered + '\
        \nSerious, critical cases: ' + serious_critical + '\
        \nCheck the link: https://www.worldometers.info/coronavirus/'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'trycatch55@gmail.com',
        'rajputonnet@gmail.com',
        msg
    )
    print('Hey Email has been sent!')

    server.quit()


bot = CoronaStats(country='China')
bot.get_data()
