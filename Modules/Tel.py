import requests
import re

class Tel:
    '''
    Class search and verify autentication telephone number
    '''    
    @staticmethod
    def ntInfo(tel):
        try:
            info = {}
            url = 'https://www.numerosdetelefono.es/'+str(tel)
            htmlTxt = requests.get(url).text
            if re.findall(r'articuloficha', htmlTxt):
                div = re.findall(r'<li(.*?)>(.*?)<\/li>', htmlTxt)
                for d in div:
                    content = d[1]
                    if content:
                        title = ''
                        lst = re.findall(r'<span.*?>(.*?)<\/span>', content)
                        if lst:
                            txt = lst[0] 
                            title = txt.replace(':','')

                        info[title] = re.sub(r'<span.*?>(.*?)<\/span>', '', content)

            return(info)
        except Exception as e:
            print('ERROR numerosdetelefono:', e)     
