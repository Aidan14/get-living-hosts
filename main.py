from data import hosts as hosts
import requests
from selenium import webdriver
import datetime
import os

CHECK_TIMEOUT = 1
PROTOCOLS = ['https'] # Change to ['http', 'https'] if you want to check both protocols
          
def check_host_alive(host, protocols=['https', 'http']):
    for protocol in protocols:
        url = f"{protocol}://{host}"

        try:
            response = requests.get(url, timeout=CHECK_TIMEOUT)
            if 200 <= response.status_code < 300:
                return True
        except requests.ConnectionError:
            pass

    return False
  
def create_output_directories(directory):
    output_path = f'./output/{directory}'
    subdirectories = ['screenshots', 'hosts', 'hosts-check']

    for subdirectory in subdirectories:
        os.makedirs(f'{output_path}/{subdirectory}', exist_ok=True)

    return output_path
  
def write_hosts_to_file(hosts, file_path):
    with open(file_path, 'a') as file:
        for host in hosts:
            file.write(f'{host}\n')
            
def check_and_take_screenshot(driver, host, output_path, protocols=['https', 'http']):
  is_alive = check_host_alive(host, protocols) 
  print(f'{host}: {is_alive}')
  
  with open(f'{output_path}/hosts-check/hosts-check.txt', 'a') as file:
    file.write(f'{host}: {is_alive}\n')
    
  if is_alive:
    for protocol in protocols:
        url = f"{protocol}://{host}"

        try:
            driver.get(url)
            screenshot_path = os.path.join(output_path, 'screenshots', f'{host}.png')
            driver.save_screenshot(screenshot_path)
            break
        except Exception as e:
            print(f"Failed to capture screenshot for {url}: {e}")
      
def main():
  # Change Chrome for your preferred Browser
  options = webdriver.ChromeOptions()
  options.add_argument('--headless') # Runs it without GUI
  driver = webdriver.Chrome(options=options)
  os.system('cls')
  
  directory = input('Insert output directory \n')
  directory = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") if directory == "" else directory
  print (f'Output directory: {directory}')
  print('')
  output_path = create_output_directories(directory)
  
  write_hosts_to_file(hosts, f'{output_path}/hosts/hosts.txt')
  
  for host in hosts:
    check_and_take_screenshot(driver, host, output_path, PROTOCOLS)
    
  driver.quit()
  print('\nProcess Completed')
  
if __name__ == '__main__':
  main()