import requests
from bs4 import BeautifulSoup

print("PLease specify your topic of desire: ")


def req_topic():
    global usr_input
    global context
    global first
    global zero
    usr_input = input()
    page = requests.get('https://en.wikipedia.org/wiki/' + str(usr_input)).text
    soup = BeautifulSoup(page, 'lxml')
    zero = soup.find("div", class_="mw-body-content")

    while usr_input not in zero.text:
        print("Unfortunately we could not find the desired topic.\nPlease specify a diffrent one:")
        print("HI")
        req_topic()

    while "may refer to:" in zero.text:
        print("Unfortunately the desired topic is not available.\nPlease specify a diffrent one: ")
        req_topic()
    while "commonly refers to:" in zero.text:
        print("Unfortunately the desired topic is not available.\nPlease specify a diffrent one: ")
        req_topic()
    while "primarily refers to:" in zero.text:
        print("Unfortunately the desired topic is not available.\nPlease specify a diffrent one: ")
        req_topic()
    while "often refers to:" in zero.text:
        print("Unfortunately the desired topic is not available.\nPlease specify a diffrent one: ")
        req_topic()
    # while "Wikipedia's sister projects:" in zero.text:
    #     print("Unfortunately the desired topic is not available.\nPlease specify a diffrent one: ")
    #     req_topic()


req_topic()

first = zero.find("div", class_="mw-parser-output")
context = first.find_all('p')

if usr_input in context[0].text:
    result = context[0].text
elif usr_input.capitalize() in context[0].text:
    result = context[0].text
else:
    result = context[1].text

print("\nFull text: " + result)

result = result.replace("  ", " ")
result = result.replace("e.g.", "for exapmle")

i = 0
while i < 50:
    result = result.replace("[" + str(i) + "]", "")
    i += 1
k = 0
while k < 50:
    result = result.replace("[nb " + str(k) + "]", "")
    k += 1

i = 0
while i < len(result):
    if result[i].isascii():
        i += 1
    else:
        result = result.replace(result[i], "")

i = 0
while i < len(result):
    if result[i] == ".":
        i += 2
        print(".")
    else:
        print(result[i], end='')
        i += 1


# IMPORTANT PART BELOW!!!
line_array = ["" for i in range(result.count("."))]
f = 0
k = 0
while f < len(result):
    print(result[f])
    if result[f] == ".":
        f += 2
        line_array[k] += "."
        k += 1
    else:
        line_array[k] += result[f]
        f += 1

try:
    print(line_array[len(line_array)])
except:
    print("End of the line")
