
class Azure:
     cost = 0.75 # class attribuates 
     def __init__(self,configuration): #  configuration -1 
         
         self.configuration = configuration
         # instance variables 
         # Inside a object we create variable  configuration -2 
         # data inside 
         
     def vmpurchase(self):
         
            if self.configuration["os"] == "ubuntu" and self.configuration["ram"] == "16 gb" and self.configuration["cpu"] == "i7":
              Azure.cost = Azure.cost + 0.25
              print("ubuntu config")
            elif self.configuration["os"] == "widnows" and self.configuration["ram"] == "8 gb" and self.configuration["cpu"] == "i5":
             Azure.cost = Azure.cost + 0.50
             print("windows config")
            elif self.configuration["os"] == "linux" and self.configuration["ram"] == "8 gb" and self.configuration["cpu"] == "i5": 
             Azure.cost = Azure.cost + 1.00 
             print("linux config")
             
            return {"vmid": "vm1234","totalcost": Azure.cost}


# execute create object and pass input and call methods
Praveen=Azure({"os":"ubuntu","ram":"16 gb","cpu":"i7","storage":"1 tb"})
ret=Praveen.vmpurchase()
print(ret)

