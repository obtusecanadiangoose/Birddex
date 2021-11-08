import json
#Data to be written
dict ={
    "name" : "Haider imtiaz",
    "rollno" : 4200,
    "cgpa" : 8.6,
    "phonenumber" : "9976770500"
}
json_data=json.dumps(dict, indent = 4)
with open("test.json", "w") as outfile:
    outfile.write(json_data)