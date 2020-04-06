def add(*args):
    s=0
    for arg in args:
        s += arg
    return print(s)

x=[]
while True:
    num = input("type nums: (if you want to finish, press \"E\")")
    if num == "E":
        break
    try:
        x.append(float(num))
    except:
        print("please type only real number")        
    
if len(x) == 0:
    print("at least type a number")
else:
    add(*x)


