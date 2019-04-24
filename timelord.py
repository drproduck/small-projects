import time
import datetime
import json
import math
import traceback

fname = 'myschedule.json'


def get_day_and_second():
  t = time.time()
  day = int(t / 86400)
  second = t - day * 86400
  if second > 0: day += 1

  return str(day), str(second)


def save_and_exit(fname=None, data=None, how='disrupt'):
  if how == "disrupt":
    print('Exiting..')

  elif how == "normal":
    with open(fname, 'w') as f:
      json.dump(data, f)

    print('Log in complete. Exiting..')

  raise SystemExit


def print_warn_msg(level):
  if level > 0: print('You are not being consistent! Please log in daily')


def get_nth_daily_login(today, daily_log):
  if today in daily_log:
    return len(daily_log[today])
  
  else: return 0



def get_summary(daily_log, history_in_days):
  last_day_used = max(history_in_days)
  n_days_passed = get_total_days() - last_day_used
  print('last used {:%d} days ago'.format(n_days_passed))
  print_warn_msg(n_days_passed)

  

while 1:
  try:
    with open(fname) as f:
      data = json.load(f)
    break 

  except:
    
    option = input('Schedule log not found, create one? (y/n): ').lower()
    if option == 'y':
      f = open(fname, 'w+')
      json.dump({'daily_log': {}}, f)
      f.close()
      continue

    else: 
      save_and_exit()


daily_log = data['daily_log']
history_in_days = list(daily_log.keys())
today, second = get_day_and_second()
nth_daily_login = get_nth_daily_login(today, daily_log)

print('Logging daily activity')

if nth_daily_login == 0:
  print('Good day commander! Be productive')
  daily_log[today] = {}
  daily_log[today][second] = 0

else:
  option = input('You have logged in {} time(s) today. Is it a serious update? (y/n): '.format(nth_daily_login)).lower()
  if option != 'y':
    save_and_exit()

  while 1:
    hours_worked = input('Please enter number of hours worked since the last log in: ')
    try: 
      hours_worked = float(hours_worked)
    except:
      print('invalid time entered. Please try again')
      continue

    if hours_worked <= 0 or hours_worked >= 24:
      print('invalid time entered. Please try again')
      continue

    break

  daily_log[today][second] = hours_worked * 3600  

save_and_exit(fname, data, 'normal')
