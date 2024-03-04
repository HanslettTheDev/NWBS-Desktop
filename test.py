### A small python script to generate the weeks of a month based on the year 
### and month

# Steps to solve this problem
# - create a dictionary that maps months to numbers e.g January = 0
# - get the first day of the month and last day of that month
# - loop through all the months and add 7 on each of the days
# - check if the current day is equal to the final day of the month
# - reset the counter to 0 and add one more for the last week
# - have a counter check to check for months which end on the 30th or 31st
    # because there are months that won't end on the 30th and extend to the next month 
# - Lastly just return the weeks and test the function

# March -> ['1-7', '8-14', '15-21', '22-28', '29-5']

import calendar

def get_weeks(year: int, month: int):
    month_dict = {name: num for num, name in enumerate(calendar.month_name) if num}
    month = month_dict[month]
    
    all_weeks = calendar.Calendar().monthdayscalendar(year, month)

    weeks = []

    for items in all_weeks:
        if items[0] == 0:
            continue
        if items[-1] == 0:
            non_zero_weeks = [x for x in items if x != 0]
            count = 1
            while len(non_zero_weeks) != 7:
                non_zero_weeks.append(count)
                count += 1
            weeks.append(f"{non_zero_weeks[0]}-{non_zero_weeks[-1]}")
            continue
        weeks.append(f"{items[0]}-{items[-1]}")

    return weeks

