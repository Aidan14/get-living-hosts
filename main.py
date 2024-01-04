from data import hosts as hosts
import requests
from selenium import webdriver
import datetime
import os
import time


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
  directory = input('Insert output directory \n')
  directory = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") if directory == "" else directory
  
  output_path = f'./output/{directory}'
  
  if not os.path.exists(output_path):
    os.mkdir(output_path)
  
  while not os.path.exists(output_path):
    print(f"Creating directory '{directory}'...")
    time.sleep(1)
  
  if not os.path.exists(f'{output_path}/screenshots'):
    os.mkdir(f'{output_path}/screenshots')
    
  if not os.path.exists(f'{output_path}/hosts'):
    os.mkdir(f'{output_path}/hosts')
    
  if not os.path.exists(f'{output_path}/hosts-check'):
    os.mkdir(f'{output_path}/hosts-check')
    
  while not os.path.exists(f'{output_path}/screenshots') and not os.path.exists(f'{output_path}/hosts') and not os.path.exists(f'{output_path}/hosts-check'):
    print(f"Creating subdirectories...")
    time.sleep(1)
    
  for host in hosts:
    with open(f'{output_path}/hosts/hosts.txt', 'a') as file:
      file.write(f'{host}\n')
      
    isAlive = check_host_alive(host)
    print(f'{host}: {isAlive}')
    with open(f'{output_path}/hosts-check/hosts-check.txt', 'a') as file:
      file.write(f'{host}: {isAlive}\n')
    
    if isAlive:
            
      http_url = f"http://{host}"
      https_url = f"https://{host}"
      try:
          driver.get(https_url)
          driver.save_screenshot(f'{output_path}/screenshots/{host}.png')
          
      except:
          driver.get(http_url)
          driver.save_screenshot(f'{output_path}/screenshots/{host}.png')
          
  driver.quit()
  
if __name__ == '__main__':
  main()