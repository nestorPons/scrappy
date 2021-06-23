import re 


class My:

    @staticmethod
    def normalize(target_str, quot=True, capital=True, special=True):
        """
        Normalizes a text for its correct comparison, removes accents and capital letters 

        Args:
            str1 (string): Text to normalize
        """
        res_str = target_str
        
        if special:
            res_str = res_str.replace('/','\/')
        if quot:
            res_str = re.sub(r"\s+", " ", res_str)
            res_str = re.sub(r"á|à", "a", res_str)
            res_str = re.sub(r"é|è", "e", res_str)
            res_str = re.sub(r"í|ì", "i", res_str)
            res_str = re.sub(r"ó|ò", "o", res_str)
            res_str = re.sub(r"ú|ù", "e", res_str)
        if capital:
            res_str = res_str.lower()
        
        res_str = res_str.strip()
                
        return res_str

    @staticmethod
    def strip_tags(value, incom=False):
        str1 = re.sub(r'<[^>]*?>', '', value)
        if incom:
            pos = str1.find('>')
            if pos != -1 :
                str1 = str1[pos+1:] 
            
            pos = str1.find('<')
            if pos != -1 :
                str1 = str1[:pos]

        return str1