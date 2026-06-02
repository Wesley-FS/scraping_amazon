from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()

options.add_argument(r"--user-data-dir=C:\ChromeBot")
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=148,
    options=options,
    use_subprocess=True
)

driver.get("https://x.com/home")

time.sleep(10)

inputs = driver.find_elements(By.TAG_NAME, "input")

print(f"\nTOTAL DE INPUTS: {len(inputs)}")

for i, inp in enumerate(inputs):
    try:
        print("\n" + "=" * 80)
        print(f"INPUT {i}")
        print("=" * 80)
        print(inp.get_attribute("outerHTML"))
    except Exception as e:
        print(f"Erro no input {i}: {e}")

input("\nENTER para fechar...")
driver.quit()