import sys
def sizeof_fmt(content, suffix='B'):
    size = sys.getsizeof(content)
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Yi', suffix)
