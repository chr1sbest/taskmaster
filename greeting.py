import datetime 
def hour_now():
    """Returns the current hour"""
    now = datetime.datetime.now().time()
    return now.hour

def greeting(hour):
    if hour < 11 and hour > 5:
        print "Good Morning Chris!"
    elif hour < 17 and hour > 5:
        print "Good Afternoon, Chris"
    else:
        print "Good Evening, Chris"

greeting(hour_now())

