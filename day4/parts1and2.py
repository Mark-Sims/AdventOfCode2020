import sys, os
import re

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')


paragraphs = AoCParser(abs_input_filepath).parse_as_list_of_paragraphs()

cleaned_passports = []
for passport in paragraphs:
    passport_fields = []
    for passport_line in passport:
        passport_fields = passport_fields + passport_line.split()

    cleaned_passports.append(passport_fields)

class Height:
    def __init__(self, height_string):
        self.unit = None
        self.value = int(re.findall(r'\d+', height_string)[0])
        if "cm" in height_string:
            self.unit = 'cm'
        if 'in' in height_string:
            self.unit = 'in'


class Passport:
    def __init__(self, passport_fields):

        self.BirthYear = None
        self.IssueYear = None
        self.ExpirationYear = None
        self.Height = None
        self.HairColor = None
        self.EyeColor = None
        self.PassportID = None
        self.CountryID = None

        self.passport_fields_map = {}
        for field in passport_fields:
            [field_key, field_val] = field.split(':') # Unpack the list returned from split()
            self.passport_fields_map[field_key] = field_val

        # Assuming all values are of the correct type
        if 'byr' in self.passport_fields_map:
            self.BirthYear = int(self.passport_fields_map['byr'])
        if 'iyr' in self.passport_fields_map:
            self.IssueYear = int(self.passport_fields_map['iyr'])
        if 'eyr' in self.passport_fields_map:
            self.ExpirationYear = int(self.passport_fields_map['eyr'])
        if 'hgt' in self.passport_fields_map:
            self.Height = Height(self.passport_fields_map['hgt'])
        if 'hcl' in self.passport_fields_map:
            self.HairColor = self.passport_fields_map['hcl']
        if 'ecl' in self.passport_fields_map:
            self.EyeColor = self.passport_fields_map['ecl']
        if 'pid' in self.passport_fields_map:
            self.PassportID = self.passport_fields_map['pid']
        if 'cid' in self.passport_fields_map:
            self.CountryID = self.passport_fields_map['cid']

    def validate_passport(self):
        if self.BirthYear and \
           self.IssueYear and \
           self.ExpirationYear and \
           self.Height and \
           self.HairColor and \
           self.EyeColor and \
           self.PassportID:
            if self.BirthYear >= 1920 and self.BirthYear <= 2002 and \
               self.IssueYear >= 2010 and self.IssueYear <= 2020 and \
               self.ExpirationYear >= 2020 and self.ExpirationYear <= 2030:
                if (self.Height.unit == 'cm' and self.Height.value >= 150 and self.Height.value <= 193) or \
                   (self.Height.unit == 'in' and self.Height.value >= 59  and self.Height.value <= 76):
                    if re.match('^#[a-f0-9]{6}$', self.HairColor):
                        if re.match('(amb|blu|brn|gry|grn|hzl|oth)', self.EyeColor):
                            if re.match('^\d{9}$', self.PassportID):
                                return True
                else:
                    return False
        return False
        

valid_passports = 0
for passport in cleaned_passports:
    if Passport(passport).validate_passport():
        valid_passports += 1

print(valid_passports) 