from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  # returns a DeclarativeMeta class
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta


#======================= create database and connection ====================#


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
menu = None
today = datetime.today()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# call the create_all method on the variable engine
Base.metadata.create_all(engine)

# ============================== functions =======================#

def menus():

    global menu
    menu = int(input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\nPlease enter your selection: \n"))


def tasks_for_today():
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print("Today", today.day, today.strftime("%b"), ":")
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        task_number = 1
        for row in rows:
            print(f" {task_number}. {row}")
            task_number += 1

    print(" ")


def tasks_week():
    # Printing the day
    day = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    for i in range(7):
        i = today + timedelta(days=i)
        # day_of_week = day[i.isoweekday()]
        print(day[i.isoweekday()], i.strftime("%d %b"), ":")

    # printing tasks

        rows = session.query(Table).filter(Table.deadline == i.date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            task_number = 1
            for row in rows:
                print(f" {task_number}. {row}")
                task_number += 1

        print("\n")


def all_tasks():
    rows = session.query(Table).all()
    rows = session.query(Table).order_by(Table.deadline).all()
    task_number = 1
    for row in rows:
        row_time = row.deadline
        print(f'{task_number}. {row}. {row_time.strftime("%#d %b")}')
        task_number += 1
    print("\n")


def add_task():
    try:

        new_task = input("Enter a task:  ")
        date = input("Enter a deadline:  ")

        if "." in date:
           new_deadline = date.replace(".", "-")


        new_deadline = datetime.strptime(new_deadline, "%d-%m-%Y")  #"%Y-%m-%d"

        new_row = Table(task= new_task, deadline=datetime.date(new_deadline))
        session.add(new_row)
        session.commit()

        print(f"\n The task: {new_task} on the date:  {date} has been added!\n ")


    except:
        print("Enter deadline in the format : dd.mm.yyyy")
        add_task()


def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()

    if len(rows) == 0:
        print("Nothing to delete")
    else:
        task_number = 1
        for row in rows:
            row_time = row.deadline
            print(f'{task_number}. {row}. {row_time.strftime("%#d %b")}')
            task_number += 1
        print("\n")
        delete_task = rows[int(input("Choose the number of the task you want to delete:"))-1]
        session.delete(delete_task)
        print("The task has been deleted!")
        session.commit()


def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    print("Missed tasks:")
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        task_number = 1
        for row in rows:
            row_time = row.deadline
            print(f'{task_number}. {row}. {row_time.strftime("%#d %b")}')
            task_number += 1
        print("\n")

# ===================== main ============================#

menus()

Session = sessionmaker(bind=engine)
session = Session()

while menu != 0:
    if menu == 1:
        tasks_for_today()
        menus()

    elif menu == 2:
        tasks_week()
        menus()

    elif menu == 3:
        all_tasks()
        menus()

    elif menu == 5:
        add_task()
        menus()

    elif menu == 4:
        missed_tasks()
        menus()


    elif menu == 6:
        delete_task()
        menus()
else:
    print("Bye!")


