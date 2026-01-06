
# code prrovided by microsoft as library 
# Resuablity of code - Microsft 

def   Vmpurchase( configuration ): # configuration -1 data varies 
    
     cost = 0.75 
     
     # code is not scalable works on ubuntu
     if configuration["os"] == "ubuntu" and configuration["ram"] == "16 gb" and configuration["cpu"] == "i7":
            cost = cost + 0.25
            print("ubuntu config")
     elif configuration["os"] == "widnows" and configuration["ram"] == "8 gb" and configuration["cpu"] == "i5":
            cost = cost + 0.50
            print("windows config")
     elif configuration["os"] == "linux" and configuration["ram"] == "8 gb" and configuration["cpu"] == "i5": 
            cost = cost + 1.00 
            print("linux config")
            
     match configuration["storage"]:
            case "1 tb":
                cost = 100.00 + cost
         
     return {"vmid": "vm1234","totalcost": cost}
 

# customer code
customersystem= {"os":"ubuntu","ram":"16 gb","cpu":"i7","storage":"1 tb"}
retval = Vmpurchase( customersystem )
print( retval )    

    
def vmpruchaseentirpese(customersystem):
    
    allconfig=[{"os":"ubuntu","ram":"16 gb","cpu":"i7","storage":"1 tb"},
               {"os":"widnows","ram":"8 gb","cpu":"i5","storage":"1 tb"},
               {"os":"linux","ram":"8 gb","cpu":"i5","storage":"1 tb"}]
    
    if customersystem in allconfig:
        print("valid ",customersystem)
        


vmpruchaseentirpese(customersystem= {"os":"ubuntu","ram":"16 gb","cpu":"i7","storage":"1 tb"})

