
a = 0

weather = "unavailable"

try:
    a = a + "hello"
    weather = "whatever"
except Exception as e:
    print(e)
    print("an error happened!")

print(a)