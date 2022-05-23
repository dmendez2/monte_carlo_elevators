import numpy as np
import math
import time
import copy 

#Treating each guest's trip as an independent event and encapsulating it in the class Trip
class Trip:
    #Trip constructor which initializes variables for Trip class
    def __init__(self,start,destination):
        self.start_floor = start
        self.destination_floor = destination
        self.distance = abs(destination-start)

#The elevator class simulates an elevator moving up and down to pick up guests and take them on their trip
class Elevator:
    #Elevator constructor which initializes the list of trips for the elevator (empty) and the run time (set to 0 initially)
    def __init__(self):
      self.trip_list=[]
      self.run_time = 0
    
    #Function to randomly create 10 guests with a random start and end floor
    def initialize_trips(self):
      #Measuring the start time
      start_time = time.time()
      i = 0
      #Looping for 10 guests
      while(i<10):
         #Random start floor for guest i
         start = np.random.randint(0,101)
         n = 0
         #Loop to make sure destination and start floor do not match
         while(n == 0):
            #Random destination floor for guest i
            destination = np.random.randint(0,101)
            #If destination and start do not match then exit the loop
            if(destination != start):
               n = 1
        #Create a new trip with this start floor and destination floor and add to the trip list
         new_trip = Trip(start,destination)
         self.trip_list.append(new_trip)
         i+=1
      #Measure the end time
      end_time = time.time()
      #Total run time of program is end time - start time
      self.run_time = end_time-start_time

#Function to find distance of following the current trip list
    def find_distance(self):
    #Elevator starts at floor 0
      distance_traveled = 0
      current_floor = 0
      for x in self.trip_list:
        #The distance travelled is the distance for the elevator to go from its current floor to the start floor of the ith guest
        #Add to this the distance of each trip to go from the start floor to the destination floor
         distance_traveled += abs(x.start_floor - current_floor)
         distance_traveled += x.distance
         #The new current floor is the current destination floor
         current_floor = x.destination_floor
      return distance_traveled

#Swaps values in trip list given two indicies to switch
    def swap(self,index1, index2):
        #Saves values of trip from index 1 in trip list
       temp_start_floor = self.trip_list[index1].start_floor
       temp_destination_floor = self.trip_list[index1].destination_floor
       temp_distance = self.trip_list[index1].distance 
         
       #Places values of index 2 into index 1 in trip list
       self.trip_list[index1].start_floor = self.trip_list[index2].start_floor
       self.trip_list[index1].destination_floor = self.trip_list[index2].destination_floor
       self.trip_list[index1].distance  = self.trip_list[index2].distance 
      
       #Places values of index 1 into index 2 in trip list 
       self.trip_list[index2].start_floor = temp_start_floor
       self.trip_list[index2].destination_floor = temp_destination_floor
       self.trip_list[index2].distance  = temp_distance 

    def optimize_trip_MCMC(self):
       start_time = time.time()
       n = 1
       long_term_distance = 0
       while(n < 1001):
           #The current "long term distance" is reset if n = 1
          if n == 1:
              long_term_distance = self.find_distance()
          
          #Chooses two random indicies
          random_index_1 = np.random.randint(0,10)
          random_index_2 = np.random.randint(0,10)
          
          #Makes sure that the two indicies do not match
          while(random_index_1 == random_index_2):
              random_index_2 = np.random.randint(0,10)

        #Swaps the trips at index 1 and index 2
          self.swap(random_index_1, random_index_2)
          #Calculates the new_distance after the swap 
          new_distance = self.find_distance()

          #If therere was no change in distance then add 1 to n
          if new_distance == long_term_distance:
              n += 1
        #If the new distance is smaller then reset n to 1 and keep the swap
          elif new_distance < long_term_distance:
              n = 1
        #If the new distance is larger then do not accept the swap and add 1 to n
          elif new_distance > long_term_distance:
              self.swap(random_index_2, random_index_1)
              n += 1
       end_time = time.time()
       #Total run time is end time - start time
       self.run_time = end_time-start_time

    def optimize_trip_MCMC_anneal(self):
       start_time = time.time()
       long_term_distance = 0
       n = 1
       while(n < 1001):
          #The current "long term" distance is reset if n=1 
          if n == 1:
            long_term_distance = self.find_distance()
        
        #Choose two random indices and make sure the two indices do not match
          random_index_1 = np.random.randint(0,10)
          random_index_2 = np.random.randint(0,10)

          while(random_index_1 == random_index_2):
             random_index_2 = np.random.randint(0,10)

         #Swap the values at the two index values
         #Calculate the new distance traveled and the change in distance between the two trip lists
          self.swap(random_index_1, random_index_2)
          new_distance = self.find_distance()
          change_in_distance = abs(long_term_distance-new_distance)

          #Assigning the alpha factor a probability according to what n is at the moment and what the change in distance is
          #When n is small, we are fine with accepting some changes in distance which are large
          #When n is larger, we will only accept changes in distance which are small
          #Eventually we will no longer accept changes which result in a larger distance traveled when n becomes large enough
          if n < 10:
              if change_in_distance < 100:
                  alpha_factor = np.random.randint(0,5)
              else:
                  alpha_factor = np.random.randint(0,100)
          if n < 20:
              if change_in_distance < 60:
                  alpha_factor = np.random.randint(0,5)
              else:
                  alpha_factor = np.random.randint(0,100)
          elif n > 20 and n <50:
              if change_in_distance < 40:
                  alpha_factor = np.random.randint(0,5)
              else:
                  alpha_factor = np.random.randint(0,100)
          elif n > 50 and n < 100:
              if change_in_distance < 20:
                  alpha_factor = np.random.randint(0,5)
              else:
                  alpha_factor = np.random.randint(0,1000)
          elif n > 100 and n < 150:
              if change_in_distance < 5:
                  alpha_factor = np.random.randint(0,5)
              else:
                  alpha_factor = np.random.randint(0,1000)
          else:
              alpha_factor = 0

          #If the new distance equals the long term distance then add 1
          if new_distance == long_term_distance:
             n += 1
          #If the new distance is less than the long term distance then accept the switch
          elif new_distance < long_term_distance:
             n = 1
          elif new_distance > long_term_distance:
             #If the new distance is greater than the long term distance then reject the change with probability (1-alpha)
             if alpha_factor != 1 or n == 1000:
                 self.swap(random_index_2, random_index_1)
                 n += 1
             #If the new distance is greater than the long term distance then accept the change with probability (alpha)
             else:
                 n = 1
       end_time = time.time()
       #Runtime of program is end time - start time
       self.run_time = end_time - start_time

    #Function to print out the trip that the elevator takes, the distance it took to make the trip, and the run time it took to optimize the trip plan
    def print_trip(self):
       current_floor = 0
       trip_number = 0
       for x in self.trip_list:
          print(trip_number,":  ",current_floor, ", ", x.start_floor)
          trip_number += 1
          print(trip_number,":  ",x.start_floor, ", ", x.destination_floor)
          current_floor = x.destination_floor
          trip_number += 1
       distance = self.find_distance()
       print("Distance of Trip: ",distance)
       print("Run Time of Program Was: ",self.run_time," seconds")

elevator_test = Elevator()
elevator_test.initialize_trips()
elevator2_test = copy.deepcopy(elevator_test)

print("Original Randomly Created Trip:" )
elevator_test.print_trip()
print()

print("Optimized Trip Using MCMC Algorithm")
elevator_test.optimize_trip_MCMC()
elevator_test.print_trip()
print()

print("Optimized Trip Using MCMC Algorithm with Annealing:")
elevator2_test.optimize_trip_MCMC_anneal()
elevator2_test.print_trip()
