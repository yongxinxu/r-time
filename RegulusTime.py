from copy import deepcopy


class TimeRepresentedBySeconds:
    def __init__(self,totalSeconds):
        precondition(isInteger(totalSeconds))
        self.allSeconds = totalSeconds

    
    def minutesUntil(self, other):
        seconds_until = other.allSeconds - self.allSeconds
        return (seconds_until // 60)  
      
        
    def addMinutes(self, minutes):
        precondition(isInteger(minutes))
        add_seconds = minutes * 60
        self.allSeconds += add_seconds
          
    
    def __repr__(self):
        return "Time(" + str(self.allSeconds) + ")"    
    

    def __str__(self):
        # First to check RDT/RST and adjust the HOURS...
        if self.allSeconds % 31104000 > 7783200 and self.allSeconds % 31104000 < 23335200: #7783200 is the all seconds at 2am, April 1, and 23335200 is at 3am, October 1.
            self_allSeconds = self.allSeconds + 3600 # inside this period, add an hour to the total time
            self.RXT = "RDT"
        else:
            self.RXT = "RST"
            self_allSeconds = self.allSeconds
            
        # Now change to calendar form...
        justSeconds = self_allSeconds % 60
        justMinutes = (self_allSeconds // 60) % 60
        justHours = (self_allSeconds // 3600) % 24     # 3600 == 60 * 60
        justDays = (self_allSeconds // 86400) % 30 + 1    # 86400 == 60 * 60 * 24
        justMonths = (self_allSeconds // 2592000) % 12 + 1 # 2592000 == 60 * 60 * 24 * 30
        justYears = (self_allSeconds // 31104000) + 1     # 31104000 == 60 * 60 * 24 * 30 * 12

        # Decide AM/PM...
        if justHours == 0:
            justHours = 12  
            self.XM = "AM"
        elif justHours < 12:
            self.XM = "AM"
        elif justHours == 12:
            self.XM = "PM"
        elif justHours > 12:
            self.XM = "PM"
            justHours = justHours - 12
        
        
        return str(justMonths) + "/" + str(justDays).zfill(2) + "/" + str(justYears).zfill(2) + " " + str(justHours) + ":" + str(justMinutes).zfill(2) + ":" + str(justSeconds).zfill(2) + " " + self.XM + " " + self.RXT
    
        
        
        
       

class TimeRepresentedByClockAndCalendar:
    def __init__(self,totalSeconds):
        precondition(isInteger(totalSeconds))
        self.AllSeconds = totalSeconds
        self.justSeconds = totalSeconds % 60
        self.justMinutes = (totalSeconds // 60) % 60
        self.justHours = (totalSeconds // 3600) % 24     # 3600 == 60 * 60
        self.justDays = (totalSeconds // 86400) % 30 + 1    # 86400 == 60 * 60 * 24
        self.justMonths = (totalSeconds // 2592000) % 12 + 1 # 2592000 == 60 * 60 * 24 * 30
        self.justYears = (totalSeconds // 31104000) + 1     # 31104000 == 60 * 60 * 24 * 30 * 12
        
        # to make the first judgment of RDT/RST
        if (self.justMonths == 4 and self.justDays == 1 and self.justHours >= 2) \
            or (self.justMonths == 4 and self.justDays > 1) or (4< self.justMonths < 10) \
            or (self.justMonths == 10 and self.justDays == 1 and self.justHours < 3): # The period between 2am, April 1 and 3am, October 1.
            self.justHours += 1
            self.RXT = "RDT"
        
        else:
            self.RXT = "RST"
    
    # To adjust time back to the normal calendar form in case of negative number( 10:-1:-3) or big number (10:87:68)...
    def time_adjustment(self):
        if self.justSeconds < 0:
            self.justMinutes -= (abs(self.justSeconds) // 60 + 1) 
            self.justSeconds = 60 - (abs(self.justSeconds) % 60)
        else:
            self.justMinutes += self.justSeconds // 60
            self.justSeconds = self.justSeconds % 60
        
        if self.justMinutes < 0:
            self.justHours -= (abs(self.justMinutes) // 60 + 1)
            self.justMinutes = 60 - (abs(self.justMinutes) % 60)
        else:
            self.justHours += self.justMinutes // 60
            self.justMinutes = self.justMinutes % 60
            
        if self.justHours < 0:
            self.justDays -= (abs(self.justHours) // 24 + 1)
            self.justHours = 24 - (abs(self.justHours) % 24)
        else:
            self.justDays += self.justHours // 24
            self.justHours = self.justHours % 24
        
        if self.justDays <= 0:
            self.justMonths -= (abs(self.justDays) // 30 + 1)
            self.justDays = 30 - (abs(self.justDays) % 30)
        else:
            self.justMonths += self.justDays // 30
            self.justDays = self.justDays % 30
        
        if self.justMonths <= 0:
            self.justYears -= (abs(self.justMonths) // 12 + 1)
            self.justMonths = 12 - (abs(self.justMonths) % 12)
        else:
            self.justYears += self.justMonths // 12
            self.justMonths = self.justMonths % 12
            
        
                
    # After the calculation of time (ex. addMinutes), to check RST/RDT again and adjust the HOURS especially when the RST/RDT of the time has changed...
    def rxt_convertion(self): 
        
        if self.RXT == "RST":
            if (self.justMonths == 4 and self.justDays == 1 and self.justHours >= 2) \
            or (self.justMonths == 4 and self.justDays > 1) or (4< self.justMonths < 10) \
            or (self.justMonths == 10 and self.justDays == 1 and self.justHours < 2):
                self.RXT = "RDT"
                self.justHours += 1
                self.time_adjustment()
        
        else:
            assert self.RXT == "RDT"
            if (self.justMonths == 4 and self.justDays == 1 and self.justHours < 3) \
            or (self.justMonths < 4) or (self.justMonths > 10)\
            or (self.justMonths == 10 and self.justDays == 1 and self.justHours >= 3)\
            or (self.justMonths == 10 and self.justDays > 1):
                self.RXT = "RST"
                self.justHours -= 1
                self.time_adjustment()
    
        
    def minutesUntil(self, other):
        MinutesUntil = 0
        MinutesUntil += (other.justMinutes - self.justMinutes)
        MinutesUntil += (other.justHours - self.justHours) * 60
        MinutesUntil += (other.justDays - self.justDays) * 24  * 60
        MinutesUntil += (other.justMonths - self.justMonths) * 30 * 24 * 60
        MinutesUntil += (other.justYears - self.justYears) * 12 * 30 * 24 * 60
        
        # when self and other have different RST/RDT, their difference in time should be adjusted by an hour
        if self.RXT == "RST" and other.RXT == "RDT":
            MinutesUntil -= 60                        # 60 mins = 1 hr
        elif self.RXT == "RDT" and other.RXT == "RST":
            MinutesUntil += 60
        
        return MinutesUntil
        
    
    def addMinutes(self, minutes):
        precondition(isInteger(minutes))
        self.justMinutes += minutes
        self.rxt_convertion()      # to check if RST/RDT is correct
        self.time_adjustment()     # to check if the expression of time is correct
        
    
    def __repr__(self):
        return "Time(" + str(self.AllSeconds) + ")"
    
        
    def __str__(self):
                self.time_adjustment()    # to check if the expression of time is correct
        self.rxt_convertion()     # to check if RST/RDT is correct
        self.time_adjustment()    # to check if the expression of time is correct after the adjustment of RST/RDT
        
        justHours = self.justHours
            
        if justHours == 0:
            justHours = 12
            self.XM = "AM"
        elif justHours < 12:
            self.XM = "AM"
        elif justHours == 12:
            self.XM = "PM"
        elif justHours > 12:
            self.XM = "PM"
            justHours -= 12
        
        
        
        return str(self.justMonths) + "/" + str(self.justDays).zfill(2) + "/" + str(self.justYears).zfill(2) + " " + str(justHours) + ":" + str(self.justMinutes).zfill(2) + ":" + str(self.justSeconds).zfill(2) + " " + self.XM + " " + self.RXT
    
