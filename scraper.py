#%% 
from bs4 import BeautifulSoup as soup
import requests
import json
import re 
import pprint
import objectpath
#%%
html_text = requests.get("https://www.youtube.com/c/LinusTechTips/videos").text
bsoup = soup(html_text, 'lxml')

#%%
# with open("ltt.html", 'w') as outfile:
#     outfile.write(bsoup.prettify())

def parse_youtube(html_text):
    expr = re.compile("var ytInitialData = (.*);")
    result = [expr.search(val.text).group(1) for val in bsoup.find_all('script') if expr.search(val.text)]
    assert len(result) == 1, print("ERROR: There should be only one page result")
    return result[0]


print(len(result))
# %%
assert len(result) == 1, print("There should be only one result")
result = result[0]
# %%

js_data = json.loads(result)
#with open("out.json",'w') as outfile:

  #  outfile.write(json.dumps(js_data))
# %%
js_tree = objectpath.Tree(js_data)
chain = js_tree.execute("$..text")
for i in chain:
    print(i)
    
# %%
