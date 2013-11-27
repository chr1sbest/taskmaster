#-----SQL Connection-----#
from datetime import date
import datetime
import sqlite3

db = sqlite3.connect('/home/chris/workspace/taskmaster/tasks.db')
cursor = db.cursor()

#-----Check for Incompletes-----#

def incomplete():
    incompletes = cursor.execute("SELECT id, task, date FROM tasktable WHERE done=0 ORDER BY date DESC") 
    print
    print 'Incomplete Tasks:'
    for entry in incompletes:
        date = datetime.datetime.strptime(entry[2],"%m-%d-%Y")
        if date < datetime.datetime.now() - datetime.timedelta(hours=24):
            print '  [ ] {:<20} {}  ({:>1})'.format(str(entry[1]),entry[2][:5],entry[0],)

if __name__ == "__main__":
    incomplete()
