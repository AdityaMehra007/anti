with open('scratch/infosys_main.js', encoding='utf-8') as f:
    text = f.read()

idx = text.find('ue.set("Cache-Control","no-cache")')
if idx != -1:
    print('Found API call snippet:')
    print(text[max(0, idx-50):min(len(text), idx+1000)])
