from selenium import webdriver
import time

driver = webdriver.Firefox()

driver.get("https://www.qimai.cn/account/signin/r/%2F")


#time.sleep(2)


driver.find_element_by_name("username").clear()
driver.find_element_by_name("username").send_keys("15513251440")

driver.find_element_by_name("password").clear()
driver.find_element_by_name("password").send_keys("huatu2018")

driver.find_element_by_css_selector("#app > div.jumbotron > div > div > form > div.submit.ivu-form-item > div > button").click()


time.sleep(2)

driver.get("https://www.qimai.cn/account/setting/type/dataCenter/page/app")

time.sleep(5)

n = 9
counter = 2
while counter <= n:
    text = driver.find_element_by_css_selector('#setting > div > div > div.router-wrapper > div > div > div.app-wraper > div:nth-child(2) > table:nth-child(3) > tbody > tr:nth-child('+str(counter)+') > td:nth-child(4) > div > div > p.num').get_attribute("textContent")
    print(text)
    counter += 1

time.sleep(15)
driver.quit()