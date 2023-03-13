import re
import handlers

OPERATIONS = {
    'hello': handlers.hello,
    'add': handlers.adding,
    'change': handlers.changing,
    'phone': handlers.get_phones,
    'show all': handlers.show_all,
    'show part': handlers.show_part,
    'remove contact': handlers.remove_contact,
    'remove phone': handlers.remove_phone,
    'days to birth': handlers.days_to_birth,
    'find': handlers.find_rec,
    'close': handlers.good_bye,
    'good bye': handlers.good_bye,
    'exit':handlers.good_bye, 
}

COMMAND_WORDS = '|'.join(OPERATIONS)

def parser(message: str) -> tuple[str|None, str|None, str|None]:
    '''
    Parse message to command, name and number.
    command: one of the COMMAND_WORD at the beginning
    date: DD.MM.YYYY at the end of the message after space
    new_number: didgits at the end of the message after space
    old_namber: didgits before new number after space
    name: all symbols between command and number
    symbols: symbols after command find,
    '''
    def clean_message(message:str, text_match:re.Match) -> tuple[str, str]:
        text = ''
        if text_match:
            text = text_match.group(1)
            message = re.sub(text, '', message)
            text = text.strip().lower()
        return message, text

    def get_number(message: str) -> re.Match:
        '''Get number as digits at the end'''
        message = message.rstrip()
        number_match = re.search(r' (\d+)$', message)
        return number_match
    
    def get_date(message: str) -> re.Match:
        '''Get date as DD.MM.YYYY at the end'''
        message = message.rstrip()
        date_match = re.search(r' (\d{2}\.\d{2}\.\d{4})$', message)
        return date_match
    
    message = message.lstrip()
    symbols_match = re.search(r'(?<=find )(\w+)\b', message, re.IGNORECASE)
    message, symbols = clean_message(message, symbols_match)

    command_match = re.search(fr'^({COMMAND_WORDS})\b', message, re.IGNORECASE)
    message, command = clean_message(message, command_match)

    date_match = get_date(message)
    message, date = clean_message(message, date_match)

    new_number_match = get_number(message)
    message, new_number = clean_message(message, new_number_match)

    old_number_match = get_number(message)
    message, old_number = clean_message(message, old_number_match)

    name = message.strip()
    return command, name, new_number, old_number, date, symbols


def main():
    address_book = handlers.address_book
    while True:
        inp = input('Write your command: ')
        command, name, new_number, old_number, date, symbols  = parser(inp)
        try:
            hendler = OPERATIONS[command]
        except KeyError:
            print('There are no command')
            continue
        output = hendler(
            name=name, 
            number=new_number, 
            old_number=old_number, 
            date=date, 
            symbols=symbols)
        print(output)
        if output == 'Good bye':
            break
    return address_book

if __name__ == '__main__':
    main()

