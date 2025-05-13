student={'name': 'Gabi' , 'age': 20, 'grade': 9.5}
for key,value in student.items():
    print(key+ ':', value)
student['age']=22
student['name']='Iancu'
student['grade']=10
print("\n")
for key,value in student.items():
    print(key+ ':', value)

