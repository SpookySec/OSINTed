import phonenumbers
import requests
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone



class PhoneNumber:
    def __init__(self, number):
        self.number = number
        parsing = phonenumbers.parse(number)
        self.country = geocoder.description_for_number(parsing, "en")
        self.carrier = carrier.name_for_number(parsing, "en")

        number = phonenumbers.format_number(
            parsing, phonenumbers.PhoneNumberFormat.E164).replace('+', '')

        numberCountryCode = phonenumbers.format_number(
            parsing, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]

        self.localNumber = phonenumbers.format_number(
            parsing, phonenumbers.PhoneNumberFormat.E164).replace(numberCountryCode, '0')
        self.internationalNumber = phonenumbers.format_number(
            parsing, phonenumbers.PhoneNumberFormat.INTERNATIONAL)