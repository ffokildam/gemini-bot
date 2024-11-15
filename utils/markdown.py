import re

def escape_markdown(text):
    text = re.sub(r'(?<!\*)\*(?!\*)', r'\\*', text)  
    return re.sub(r'([_\[\]()~>#+\-=|{}.!])', r'\\\1', text)