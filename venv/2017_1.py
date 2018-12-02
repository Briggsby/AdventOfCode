

def sum(numbers, halfway = False):
    result = 0
    n = len(numbers)
    plus = 1
    if (halfway):
        plus = int(n/2)
    for i in range(n):
        if (numbers[i] == numbers[(i+plus)%n]):
            result += numbers[i]
    return(result)

def intError(number):
    try:
        return(int(number))
    except:
        pass

def convertToNumbers(numbers):
    result = []
    app = result.append
    for n in numbers:
        try:
            app(int(n))
        except:
            pass
    return(result)

def readFile(file):
    file = open(file, 'r')
    return(file.read())

numbers = readFile('2018_1_input.txt')
numbers = convertToNumbers(numbers)
print(sum(numbers, True))
