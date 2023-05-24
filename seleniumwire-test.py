import time
# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = webdriver.ChromeOptions()
# you are going to tell selenium the IP where the code will run
# replace scrap with the IP, I use scrap because my docker-compose file uses that name
chrome_options.add_argument('--proxy-server=0.0.0.0:8087')
chrome_options.add_argument('--ignore-certificate-errors')

# driver = webdriver.Chrome(ChromeDriverManager().install())
options = {
    'auto_config': False,
    'addr': '0.0.0.0',
    'port': 8087
}
driver = webdriver.Remote(
    command_executor="http://0.0.0.0:4444/wd/hub",
    desired_capabilities=chrome_options.to_capabilities(),
    seleniumwire_options=options
)
print(driver.capabilities)

driver.get("https://www.hudl.com/login")
time.sleep(2)
driver.find_element(By.ID, "email").send_keys("ralph.gehy@hudl.com")
driver.find_element(By.CSS_SELECTOR, "button[data-qa-id='login-btn']").click()
time.sleep(15)
# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(
            f"Request URL: {request.url}\n",
            f"Response Code: {request.response.status_code}\n",
            f"Content Type: {request.response.headers['Content-Type']}\n",
            f"Cloudfront Hit: {request.response.headers['x-cache']}\n\n"
        )
driver.quit()
