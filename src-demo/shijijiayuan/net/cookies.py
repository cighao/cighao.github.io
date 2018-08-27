
def getCookies():
    f = open('cookies.txt','r')
    cookies = {}
    for line in f.readline():
        key, value = line.split('=', 1)
        cookies[key] = value
    f.close()
    print(cookies)

