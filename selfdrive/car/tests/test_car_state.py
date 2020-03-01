#!/usr/bin/env python3
import time
import cereal.messaging as messaging

def start_check():
  sm = messaging.SubMaster(['carState'])
  sm.update()

  print("Testing every car state parameter. Ctrl-C to skip to the next parameter.")

  check_signal(sm, "canValid", "Can Valid") #@26 :Bool;
  check_signal(sm, "doorOpen", "Door Open")
  check_signal(sm, "seatbeltUnlatched", "Seatbelt Unlatched")
  check_signal(sm, "buttonEvents", "Button Events")
  check_signal(sm, "leftBlinker", "Left Blinker") #@20 :Bool;
  check_signal(sm, "rightBlinker", "Right Blinker") #@21 :Bool;
  check_signal(sm, "genericToggle", "Generic Toggle") #@23 :Bool;
  check_signal(sm, "gasPressed", "Gas Pressed") #@4 :Bool;    # this is user pedal only
  check_signal(sm, "brake", "Brake") #@5 :Float32;      # this is user pedal only
  check_signal(sm, "brakePressed", "Brake Pressed") #@6 :Bool;  # this is user pedal only
  check_signal(sm, "brakeLights", "Brake Lights") #@19 :Bool;
  check_signal(sm, "gearShifter", "Gear Shifter") #@14 :GearShifter;
  check_signal(sm, "steeringAngle", "Steering Angle") #@7 :Float32;   # deg
  check_signal(sm, "steeringRate", "Steering Rate") #@15 :Float32;   # deg/s
  check_signal(sm, "steeringTorque", "Steering Torque") #@8 :Float32;  # TODO: standardize units
  check_signal(sm, "steeringTorqueEps", "Steering Torque EPS") #@27 :Float32;  # TODO: standardize units
  check_signal(sm, "steeringPressed", "Steering Pressed") #@9 :Bool;    # if the user is using the steering wheel
  check_signal(sm, "steeringRateLimited", "Steering Rate Limited") #@29 :Bool;    # if the torque is limited by the rate limiter
  check_signal(sm, "stockAeb", "Stock AEB") #@30 :Bool;
  check_signal(sm, "stockFcw", "Stock FCW") #@31 :Bool;
#  check_signal(sm, "espDisabled", "ESP Disabled") #@32 :Bool;
  check_signal(sm, "clutchPressed", "Clutch Pressed") #@28 :Bool;
  check_signal(sm, "vEgo", "vEgo") #@1 :Float32;         # best estimate of speed
  check_signal(sm, "aEgo", "aEgo") #@16 :Float32;        # best estimate of acceleration
  check_signal(sm, "vEgoRaw", "vEgo Raw") #@17 :Float32;     # unfiltered speed from CAN sensors
  check_signal(sm, "yawRate", "Yaw Rate") #@22 :Float32;     # best estimate of yaw rate
  check_signal(sm, "standstill", "Standstill") #@18 :Bool;
  check_signal(sm, "wheelSpeeds", "Wheel Speeds") #@2 :WheelSpeeds;
  check_signal(sm, "cruiseState", "Cruise State") #@10 :CruiseState;

def check_signal(sm, signal_name, desc):
  lastStatus = getattr(sm['carState'], signal_name)
  count = 0

  print("Test", desc)
  print("Current value", lastStatus)

  checking = True
  start = time.time()
  try:
    while checking:
      sm.update()

      if sm.updated['carState']:
        signal = getattr(sm['carState'], signal_name)
        if lastStatus != signal:
           lastStatus = signal
           count += 1
           print(desc, "changed", lastStatus, count)
      #if time.time() > start + 10:
        #check with user if they want to exit
        #checking = False
      if count > 5:
        checking = False
  except KeyboardInterrupt:
    print('Skipping', desc)

if __name__ == "__main__":
  start_check()
