# Data types 
      
smile = 5       # int class 
name ="ust"      # str class 
weight =56.7     # float class 
appraisal=True   # bool class 

"wow"  # data  -> type str class 
print(type(smile))

# ref count 

smile ="ust is global comapny in india" # smile points to good 
smiles1=smile 
smiles2=smiles1

import sys 
print(sys.getrefcount(smiles1))

# data structures 


# cabin is fixed space- tuple 
placesit =(67, "praveen",":smiling buddha","laptop")
print(placesit)

# team size fixed or growable - List 

team=["sandeep","arun","vamshi"]
team.append("seetha")
print(team)

# people  from city - different place - dict 

peoples={"karthik":"namkal","Ganesh":"bangalore"}
appraissal={"venkatesh":9,"ganesh":8}
peoples.update({"vamshi":"bangalore"})
print(peoples)


# In Devops Azure 

sub_id= "ab89y3y347-3343-403992-b26d-e7444"
resource_group="myresourecgroup"
vm_name="myvm"


myaccount={
    "sub_id": "ab89y3y347-3343-403992-b26d-e7444",
    "resource_group":"myresourecgroup",
    "vm_name":"myvm"
}


updateparams= {
    "location":"East-us2",
    "servcie":{
        "Capcaicty":5
    }
}

print(updateparams)