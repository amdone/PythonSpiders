import re
s1 = "https://pbs.twimg.com/media/EdbbMjFUwAAHtR7?format=jpg&name=small"

s2 = re.sub("^&name=.*?$","&name=orig",s1)
s3 = s1.replace(r'(.*)name(.*)',"name=orig")
s4 = s1.split('&')
s5=s4[0] + "&name=orig"
print(s2)
print(s3)
print(s4)
print(s5)