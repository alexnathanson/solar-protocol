
a = 0


try:
    a = a + "hello"
except Exception as e:
    print(e)
    print("an error happened!")

print(a)