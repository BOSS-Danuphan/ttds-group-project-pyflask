import sys
from urllib.request import urlopen
from urllib.error import  URLError

def sizeof_fmt(content, suffix='B'):
    size = sys.getsizeof(content)
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Yi', suffix)

def safeurlopen(url):
    content = None
    try:
        response = urlopen(url)
        content = response.read().decode('utf-8')
    except URLError as e:
        errortext = f'Failed to reach a server. url: {url}'
        if hasattr(e, 'code'):
            errortext += f' Code: {e.code}'
        if hasattr(e, 'reason'):
            errortext += f' Reason: {e.reason}'
        print(errortext)
    return content
