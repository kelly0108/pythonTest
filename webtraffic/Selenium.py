from selenium import webdriver
import time
from mitmproxy import ctx

from selenium.webdriver.support import ui

driver = webdriver.Chrome()
driver.get("https://passport.umeng.com/login")

wait = ui.WebDriverWait(driver,10)
wait.until(lambda driver: driver.find_element_by_id('alibaba-login-box'))
#driver.switch_to.frame('alibaba-login-box') #登录的iframe
#driver.find_element_by_id("fm-login-id").clear()
#driver.find_element_by_id("fm-login-id").send_keys("huatujiaoyu_pm@163.com")
#driver.find_element_by_id("fm-login-password").clear()
#driver.find_element_by_id("fm-login-password").send_keys("jiaoshizaixian")
#driver.find_element_by_id("nc_1__scale_text")

#button = driver.find_element_by_id('tcaptcha_drag_button')    # 找到“蓝色滑块”
#action = ActionChains(driver) # 实例化一个action对象
#action.click_and_hold(button).perform()  # perform()用来执行ActionChains中存储的行为
#action.reset_actions()5 | action.move_by_offset(180, 0).perform()  # 移动滑块

time.sleep(5)
#通过 submit() 来操作
#driver.find_element_by_id("fm-login-submit").submit()
time.sleep(3)

# 获得 cookie 信息
cookie= driver.get_cookies()
#将获得 cookie 的信息打印
print(cookie)
#driver.quit()
