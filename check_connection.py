import urllib3

def check_internet():
    '''
    melakukan pengecekan koneksi internet.
    fungsi akan return True apabila terdapat koneksi internet
    dan False apabila sebaliknya.
    '''
    http = urllib3.PoolManager()
    try:
        http.request('GET','http://google.com', timeout=1)
        return True
    except urllib3.exceptions.MaxRetryError:
        return False