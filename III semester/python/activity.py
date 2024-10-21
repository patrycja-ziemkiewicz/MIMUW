import heapq

activities = {}

def add_activity():
    activity = input("Enter the name of the activity: ")
    time = int(input("Enter the time spent on this activity (in minutes): "))
    if activity not in activities:
        activities[activity] = [time]
    else:
        activities[activity].append(time)

def show_time():
    activity = input("Enter the name of the activity for which you want to see the total time: ")
    if activity in activities:
        total_time = sum(activities[activity])
        print(f"Total time spent on activity '{activity}' is: {total_time} minutes")
    else:
        print(f"Activity '{activity}' not found.")

def show_top_activities():
    ranking = []
    for activity in activities:
        total_time = sum(activities[activity])
        ranking.append([total_time, activity])
    largest = heapq.nlargest(min(len(ranking), 3), ranking)
    print("Top 3 activities:")
    for i in range(len(largest)):
        print(f"{i + 1}. {largest[i][1]}: {largest[i][0]} minutes")

while True:
    print("Choose one of the options: \n\
          1 - Add a new activity \n\
          2 - Show time for a selected activity \n\
          3 - Show top 3 activities \n\
          4 - Exit the program")
    n = input()
    match n:
        case '1':
            add_activity()
        case '2':
            show_time()
        case '3':
            show_top_activities()
        case '4':
            print("Exiting the program.")
            break
        case _:
            print("Invalid option. Please try again.")