import os
from time import sleep
patchs = [
"13.1"]

for patch in patchs:
  os.system(f'scrapy runspider -a patch={patch} -O data/patch_{patch}.csv main.py')
  sleep(10)