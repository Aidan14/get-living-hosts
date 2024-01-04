from data import hosts as  hosts
import requests
from selenium import webdriver
import datetime

CHECK_TIMEOUT = 5
          
def check_host_alive(host):
    # Check HTTP availability
    http_url = f"http://{host}"
    try:
        response = requests.get(http_url, timeout=CHECK_TIMEOUT)
        return 200 <= response.status_code < 300
    except requests.ConnectionError:
      pass

    # Check HTTPS availability
    https_url = f"https://{host}"
    try:
        response = requests.get(https_url, timeout=CHECK_TIMEOUT)
        return 200 <= response.status_code < 300
    except requests.ConnectionError:
        pass
        
    return False

def main():
  # Change Chrome for your preferred Browser
  options = webdriver.ChromeOptions()
  options.add_argument('--headless') # Runs it without GUI
  driver = webdriver.Chrome(options=options)
  date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
  for host in hosts:
    with open(f'./hosts/hosts_{date}.txt', 'a') as file:
      file.write(f'{host}\n')
      
    isAlive = check_host_alive(host)
    print(f'{host}: {isAlive}')
    with open(f'./hosts-check/hosts-check_{date}.txt', 'a') as file:
      file.write(f'{host}: {isAlive}\n')
    
    if isAlive:
      output_path = f'./screenshots/{host}_{date}.png'
            
      http_url = f"http://{host}"
      https_url = f"https://{host}"
      try:
          driver.get(https_url)
          driver.save_screenshot(output_path)
          
      except:
          driver.get(http_url)
          driver.save_screenshot(output_path)
          
  driver.quit()
  
if __name__ == '__main__':
  main()