#!/usr/bin/env python3
import time
import cereal.messaging as messaging

def start_check():
  sm = messaging.SubMaster(['carState'])
  sm.update()

#  check_signal(sm, sm['carState'].canValid, "Can Valid") #@26 :Bool;
  check_signal(sm, "doorOpen", "Door Open")
  check_signal(sm, "seatbeltUnlatched", "Seatbelt Unlatched")
  check_signal(sm, "buttonEvents", "Button Events")
  check_signal(sm, "leftBlinker", "Left Blinker") #@20 :Bool;
  check_signal(sm, "rightBlinker", "Right Blinker") #@21 :Bool;
  check_signal(sm, "genericToggle", "Generic Toggle") #@23 :Bool;

def check_signal(sm, signal_name, desc):
  lastStatus = getattr(sm['carState'], signal_name)
  count = 0

  print("Test ", desc)
  print("Current value ", lastStatus)

  checking = True
  start = time.time()

  while checking:
    sm.update()

    if sm.updated['carState']:
      signal = getattr(sm['carState'], signal_name)
      if lastStatus != signal:
         lastStatus = signal
         count += 1
         print(desc, " changed ", lastStatus, count)
    if time.time() > start + 10:
      #check with user if they want to exit
      checking = False
    if count > 10:
      checking = False

if __name__ == "__main__":
  start_check()
