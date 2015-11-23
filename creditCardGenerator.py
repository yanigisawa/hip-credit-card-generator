import re
import time
import json
import entities
from bottle import route, run, template, request, response
import os 
import random


class CreditCardGenerator:
    # Name, Possible Prefix List, Length
    _credit_card_types = [("American Express", [34, 37, 373], 15),
         ("Discover Card", [6011], 16),
         ("MasterCard", range(51, 56), 16),
         ("Visa", [4], 16)
         
         ] 
    # China UnionPay  62[6]   Yes 16-19[citation needed]  Luhn algorithm
    # Diners Club Carte Blanche   300-305 Yes 14  Luhn algorithm
    # Diners Club International[7]    300-305, 309, 36    Yes 14  Luhn algorithm
    # 38-39[8]    Yes 14  Luhn algorithm
    # Diners Club United States & Canada[9]   54, 55  Yes 16  Luhn algorithm
    # InterPaymentTM  636 Yes 16-19   Luhn algorithm
    # InstaPayment    637-639[citation needed]    Yes 16  Luhn algorithm
    # JCB 3528-3589[11]   Yes 16  Luhn algorithm
    # Laser   6304, 6706, 6771, 6709  No[12]  16-19   Luhn algorithm
    # Maestro 50, 56-69 [1]   Yes 12-19   Luhn algorithm
    # Dankort 5019    Yes 16  Luhn algorithm
    # Solo    6334, 6767  No  16, 18, 19  Luhn algorithm
    # Switch  4903, 4905, 4911, 4936, 564182, 633110, 6333, 6759  No  16, 18, 19  Luhn algorithm
    # UATP    1   Yes 15  Luhn algorithm

    def get_credit_card_type(self, selectedTypeName = None):
        names = [t[0].lower() for t in self._credit_card_types]
        returnType = None
        if selectedTypeName is None or selectedTypeName.lower() not in names:
            randIndex = random.randint(0, len(self._credit_card_types) - 1)
            returnType = self._credit_card_types[randIndex]
        else:
            for t in self._credit_card_types:
                if selectedTypeName.lower() == t[0].lower():
                    returnType = t
                    break

        return returnType

    def get_check_digit(self, newNumber):
        charArr = [int(c) for c in str(newNumber)]
        count = 0
        charArr.reverse()
        digits = []
        for d in charArr[1:]:
            if count % 2 == 0:
                product = d * 2
                if product > 9:
                    digit_sum = sum([int(c) for c in str(product)])
                    digits.append(digit_sum)
                else:
                    digits.append(product)
            else:
                digits.append(d)

            count += 1

        return int(str(sum(digits) * 9)[-1:])

    def get_random_number(self, selectedType = None):
        selectedType = self.get_credit_card_type(selectedType)
        prefixInt = random.randint(0, len(selectedType[1]) - 1)
        newNumber = str(selectedType[1][prefixInt])
        length = selectedType[2] - len(newNumber)
        for i in range(length):
            newNumber += str(random.randint(0, 9))

        checkDigit = self.get_check_digit(newNumber)
        newNumber = newNumber[:-1] + str(checkDigit)
        return newNumber

def get_requested_command(message):
    cmd = message.item.message.message
    cmd = re.sub('/ccgen ', '', cmd)

    return cmd

def get_help_message():
    msg = "Generates a random credit card number. Usage:"
    msg += "<ul><li>/ccgen - Picks a random type and returns a random number</li>"
    msg += "<li>/ccgen <type> - Returns a random number for the type specified</li></ul>"
    msg += "Possible Types include: "
    msg += "<ul>"
    for tp in CreditCardGenerator._credit_card_types:
        msg += "<li>{0}</li>".format(tp[0])
    msg += "</ul>"
    return msg

@route ("/", method='POST')
def index():

    msg = entities.HipChatRoomMessage(**request.json)
    command = get_requested_command(msg)
    if re.match('^help$', command):
        response = get_help_message()
    else:
        ccg = CreditCardGenerator()
        response = ccg.get_random_number(command)
    if response != None:
        parameters = {}
        parameters['from'] = 'Credit Card Generator'
        parameters['room_id'] = msg.item.room.room_id 
        parameters['message'] = response
        parameters['color'] = 'gray'

        return json.dumps(parameters)

if __name__ == "__main__":
    run (host='localhost', port=8080, reloader=True, server='paste')
