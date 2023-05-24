import time
import boto3
from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = webdriver.ChromeOptions()
# you are going to tell selenium the IP where the code will run
# replace scrap with the IP, I use scrap because my docker-compose file uses that name
chrome_options.add_argument('--proxy-server=3.83.190.70:8087')
chrome_options.add_argument('--ignore-certificate-errors')

# driver = webdriver.Chrome(ChromeDriverManager().install())
options = {
    'auto_config': False,
    'addr': '3.83.190.70',
    'port': 8087
}
devicefarm_client = boto3.client("devicefarm")

testgrid_url_response = devicefarm_client.create_test_grid_url(
      projectArn="arn:aws:devicefarm:us-west-2:810639563432:project:f86810bd-a3a1-47f7-bdf3-7127a8b9f211",
      expiresInSeconds=300
      )


driver = webdriver.Remote(
    command_executor=testgrid_url_response,
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
