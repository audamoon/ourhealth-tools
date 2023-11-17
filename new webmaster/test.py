import re

domain_parts = re.findall(r'(https:)\/\/([a-z-.]+)[\/]?', "https://novaya-otradovka.stop-alko.com", re.IGNORECASE)[0]
print(domain_parts[1])