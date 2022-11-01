import requests
import string

def get_text(usr_input):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': usr_input,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True
        }
    ).json()
    page = next(iter(response['query']['pages'].values()))
    text = page['extract']
    return text


def run():
    usr_input = input()
    text = get_text(usr_input)
    if usr_input not in text:
        usr_input = usr_input.title()
        text = get_text(usr_input)

    print(text.replace("\n", " "))

    line_array = ["" for i in range(text.count("."))]
    f = 0
    k = 0

    while f < len(text):
        print(line_array)
        if text[f] == ".":
            if f+1 >= len(text):
                line_array[k] += "."
                break
            elif text[f+1] == " ":
                f += 2
            else:
                f += 1
            line_array[k] += "."
            k += 1
        else:
            print(k)
            print(len(line_array))
            if k+1 > len(line_array):
                break
            else:
                line_array[k] += text[f]
                f += 1





run()