from classes import Phone, Name, Birthday, Record, AdressBook
from datetime import datetime
import pickle
from pathlib import Path

CONTACTS_FILE = Path('data.bin')
if CONTACTS_FILE.exists():
    with open(CONTACTS_FILE, 'rb') as file:
        address_book = pickle.load(file)
else:
    address_book = AdressBook()
iterator = iter(address_book)


def input_error(func):
    '''Decorator that handles errors in the handlers'''
    def inner(*args, **kwargs):
        try:
            output = func(*args, **kwargs)
        except KeyError as ke:
            output = f'There are no contact {str(ke)} in contacts'
        except ValueError as ve:
            output = str(ve).capitalize()
        except AttributeError:
            output = 'There no birthday date in this contact'
        except StopIteration: 
            output = 'There are no more contacts'
        return output 
    return inner

def hello(*_) -> str:
    '''Return bots greeting'''
    output = 'How can I help you?'
    return output

@input_error
def adding(name: str, number: str, arg, date: str, *_) -> str:
    '''If contact is existing add phone to it, else create contact'''
    record = address_book.data.get(name)
    phone = Phone(number)
    name = Name(name)
    if date:
        date = datetime.strptime(date, '%d.%m.%Y').date()
        date = Birthday(date)
    if record:
        record.add_phone(phone)
        output = f'To contact {name.value} add new number: {phone.value}'
    else: 
        record = Record(name, phone, birthday=date)
        address_book.add_record(record)
        output = f'Contact {record} is saved'
    return output

@input_error
def changing(name: str, new_number: str, old_number: str, *_) -> str:
    '''Change contact in the dictionary'''
    record = address_book.data[name]
    new_phone = Phone(new_number)
    old_phone = Phone(old_number)
    record.change(old_phone, new_phone)
    output = f'Contact {name} is changed from {old_number} to {new_number}'
    return output

@input_error
def get_phones(name: str, *_) -> str:
    '''Return numbers received contact'''
    record = address_book.data[name]
    numbers = record.get_numbers()
    return numbers

@input_error
def remove_phone(name: str, number: str, *_) -> str:
    '''Remove phone from contact phone numbers'''
    record = address_book.data[name]
    phone = Phone(number)
    record.remove_phone(phone)
    output = f'Number {number} is deleted from contact {name}'
    return output

@input_error
def days_to_birth(name: str, *_) -> str:
    '''Remove phone from contact phone numbers'''
    record = address_book.data[name]
    days = record.days_to_birthday()
    output = f'To {name} birthday {days} days'
    return output

@input_error
def remove_contact(name: str, *_) -> str:
    '''Remove contact from address book'''
    address_book.data.pop(name)
    output = f'Contact {name} is deleted'
    return output

def show_all(*_) -> str:
    '''Return message with all contacts'''
    return address_book.show_records()

@input_error
def show_part(*_) -> str:
    '''Return message with n contacts'''
    return next(iterator)

def find_rec(symbols, *args):
    return address_book.find_records(symbols)

def good_bye(*args, **kwargs) -> str:
    '''Return bot goodbye'''
    output = "Good bye"
    with open(CONTACTS_FILE, 'wb') as file:
        pickle.dump(address_book, file)
    return output



