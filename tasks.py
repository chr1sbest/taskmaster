import datetime

#-----Task displaying-----#

def day_tasks(day='today'):
    """
    Return all tasks for specified day
    
    >>> day_tasks()

    Tasks for today
    -Do Laundry          (1)
    -Pick up bitches     (2)
    -Get Money           (3)
    """
    tdict = {0:' ', 1:'X' } #X if task is done
    tasks = pull_by_date(format(day)) #pull from tasks.db
    print
    print "Tasks for " + day

    if tasks:
        for task in tasks: 
            print '  [{}] {:<20} ({:>1})'.format(tdict[task[2]],str(task[1]),task[0],)

    else:
        print '--No Tasks--'
    print

def format(date):
    """
    Format different types of dates

    >>> format('today')
    '11-09-13'
    >>> format('11-09-13')
    '11-09-13'
    >>> format('tomorrow')
    '11-10-13'
    """
    if date == 'today':
        now = datetime.datetime.now()
        return '{0}-{1}-{2}'.format(now.month,now.day,now.year)
    elif date =='tomorrow':
        tom = datetime.date.today() + datetime.timedelta(hours=24)
        return '{0}-{1}-{2}'.format(tom.month,tom.day,tom.year)  
    elif date =='yesterday':
        yest = datetime.date.today() - datetime.timedelta(hours=24)
        return '{0}-{1}-{2}'.format(yest.month, yest.day, yest.year)
    else: return date

#-----Adding and Removing Tasks-----#

def add(day,*args):
    """
    Add task to specific day
    
    >>> add('today','Do laundry', 'Pick up bitches', 'Get Money')
    Tasks added to today:
    1 Do Laundry
    2 Pick up bitches
    3 Get Money
    """
    tasks_added = []
    for task in args:
        number =  new_db_entry(task,format(day)) #new SQL primary key num 
        tasks_added.append((number,task))
    print "Tasks added to {0}:".format(day)
    for tup in tasks_added:
        print tup[0], tup[1]

def remove(*args):
    """
    Change done from 0 to 1
    >>> remove('1','2','3')
    Tasks updated: [1,2,3]
    *Done* Do Laundry *Done*
    *Done* Pick up bitches *Done*
    *Done* Get Money *Done*
    """
    errorlog = []
    for number in args:
        if pull_by_num(number) == 1:
            errorlog.append('Task {0} is already complete!'.format(number))
        else:
            updated = 1
            change_by_num(number, updated) #Update in database
    if errorlog:
        print 'Errors:'
        print "\n".join(errorlog)

def undo(*args):
    """
    Remove *Done* from finished tasks
    """
    errorlog = []
    for number in args:
        if not pull_by_num(number):
            errorlog.append('Task {0} is not finished!'.format(number))
        else:
            updated = 0
            change_by_num(number, updated) #Update in database
    if errorlog:
        print 'Errors:'
        print "\n".join(errorlog)

#-----SQL Queries-----#

import sqlite3

db = sqlite3.connect('/home/chris/workspace/taskmaster/tasks.db')
cursor = db.cursor()

def main():
    pass

def createTable():
    """
    Create table titled 'tasktable'.
    """
    cursor.execute('''CREATE TABLE tasktable
    (id INTEGER PRIMARY KEY, task TEXT, date TEXT, done INT)''')

 
def new_db_entry(task, day, done=0):
    """
    SQL insert query to add a task,day,done. Return new ID.
    """
    cursor.execute('''INSERT INTO tasktable (Task,Date,Done)
                      VALUES (?,?,?)''',(task, day,done))
    db.commit()
    cursor.execute('SELECT max(id) FROM tasktable')
    return cursor.fetchone()[0]

def pull_by_date(date):
    """
    SQL query to return array of (id, task, done) that match a date.
    """
    cursor.execute("SELECT id, task, done FROM tasktable WHERE date=? ORDER BY done ASC",(format(date),))
    return cursor.fetchall()

def pull_by_num(number):
    """
    SQL query to return a task by its number.
    """
    cursor.execute("SELECT done FROM tasktable WHERE id=?",(number,))
    return str(cursor.fetchone()[0])

def change_by_num(number,updated):
    """
    SQL update query to change done value.   
    """
    cursor.execute("UPDATE tasktable SET done=? WHERE id=?",(updated,number))
    db.commit()
    return 'Success'
 
def rename(number,name):
    """
    SQL update query to change name of task
    """
    cursor.execute("UPDATE tasktable SET task=? WHERE id=?",(name,number))
    db.commit()

def move(number, date):
    """
    Move task to a certain day
    """
    cursor.execute("UPDATE tasktable SET date=? WHERE id=?",(format(date),number))
    db.commit()

#-----Argument Handler------#

import sys

def main():
    if len(sys.argv) == 1:
        return day_tasks()
    command = sys.argv[1]
    args = sys.argv[2:]
    if command  == 'for':
        return day_tasks(*args)
    elif command == 'fin':
        return remove(*args)
    elif command == 'undo':
        return undo(*args)
    elif command == 'add':
        return add(*args)
    elif command == 'name':
        return rename(*args)
    elif command == 'move':
        return move(*args)
    else:
        return 'Invalid argument'

if __name__ == "__main__":
    main()
