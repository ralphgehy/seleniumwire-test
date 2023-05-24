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

# driver = webdriver.Chrome(ChromeDriverManager().install())
options = {
    'addr': '0.0.0.0'
}
devicefarm_client = boto3.client("devicefarm", region_name="us-west-2")

testgrid_url_response = devicefarm_client.create_test_grid_url(
      projectArn="arn:aws:devicefarm:us-west-2:810639563432:testgrid-project:fea1916c-32b0-47fd-b008-804e5d7c1e7e",
      expiresInSeconds=300
      )


driver = webdriver.Remote(
    command_executor=testgrid_url_response["url"],
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
