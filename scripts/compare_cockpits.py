import re

with open('bengaluru_startup_cockpit.html', 'r', encoding='utf-8') as f:
    text = f.read()

tabs = re.findall(r'tab-btn[^\>]*onclick=[\'"]([^\'"]+)[\'"][^\>]*>([^<]+)<', text)
print('Tabs in bengaluru_startup_cockpit.html:')
for action, label in tabs:
    print(f"  Action: {action} -> Label: {label.strip()}")

with open('bengaluru_startup_intelligence_cockpit.html', 'r', encoding='utf-8') as f:
    text2 = f.read()

tabs2 = re.findall(r'tab-btn[^\>]*onclick=[\'"]([^\'"]+)[\'"][^\>]*>([^<]+)<', text2)
print('\nTabs in bengaluru_startup_intelligence_cockpit.html:')
for action, label in tabs2:
    print(f"  Action: {action} -> Label: {label.strip()}")
