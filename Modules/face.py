import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_robots(False)
br.addheaders = [("User-agent","Mozilla/5.0")]
bf = br.open('https://www.facebook.com/lebouquet.estetica/')
sc = bf.read().decode("utf-8") 
print(sc)