#-----SQL Connection-----#
from datetime import date
import datetime
import sqlite3

db = sqlite3.connect('/home/chris/workspace/taskmaster/tasks.db')
cursor = db.cursor()

#-----Check for Incompletes-----#

def incomplete():
    incompletes = cursor.execute(
        """
        SELECT id, task, date 
        FROM tasktable 
        WHERE done=0 
        ORDER BY date DESC
        """
    ) 
    print
    print 'All Tasks:'
    yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
    for entry in incompletes:
        name = str(entry[1])
        date = entry[2][:5]
        number = entry[0]
        print '  [ ] {:<20} {}  ({:>1})'.format(name, date, number)

if __name__ == "__main__":
    incomplete()
