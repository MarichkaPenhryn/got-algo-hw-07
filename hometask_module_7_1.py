
from collections import UserDict
import datetime
from datetime import datetime
from datetime import timedelta

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me 2 arguments please."
        except KeyError:
            return "User not found."
        except IndexError:
            return "Give me name please."
        except AttributeError:
            return "Invalid input"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def __init__(self, value):
        try:
            dd, mm, yyyy = map(int, value.split('.'))
            if (value[2] == '.') and (value[5] == '.'):
                self.value = datetime(year=yyyy, month=mm, day=dd).date()

        except ValueError:
            self.value = None
            print("Invalid date format. Use DD.MM.YYYY")



class Name(Field):
    pass  # Используем функционал родительского класса без изменений

class Phone(Field):
    def __init__(self, value):
        try:
            if value.isdigit() and len(value) == 10:
                self.value = value

            else: print('Phone number must be 10 digits and contain only digits')
        except ValueError:
            self.value = None


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        # Очищаем список телефонов перед добавлением нового
        self.phones.clear()
        self.phones.append(Phone(phone))


    def add_bir(self, bir: str):
        self.birthday = Birthday(bir)

    def remove_phone(self):
        # Очищаем список телефонов
        self.phones.clear()



    def find_phone(self, phone: str):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        phones_str = ', '.join(map(str, self.phones))
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        try:
            return self.data[name]
        except KeyError:
            return None

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f'There is no {name} in AddressBook')

    def get_upcoming_birthdays(self):
        now = datetime.now()
        date = datetime(year=now.year, month=now.month, day=now.day)
        congratulation_list = []

        for name, record in self.data.items():
            if record.birthday and record.birthday.value:
                user_birth = record.birthday.value
                user_birth_this_year = datetime(year=now.year, month=user_birth.month, day=user_birth.day)

                user_congrats_day = datetime(year=now.year, month=user_birth.month, day=user_birth.day)
                if date <= user_birth_this_year < date + timedelta(days=7):
                    if user_congrats_day.weekday() == 5:
                        user_congrats_day += timedelta(days=2)
                    elif user_congrats_day.weekday() == 6:
                        user_congrats_day += timedelta(days=1)

                    congratulation_list.append({'name': name, 'congratulation_date': user_congrats_day.strftime("%Y-%m-%d")})

        return congratulation_list





@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        new_phone = Phone(phone)
        if new_phone.value is None:
            message = f"Contact not added. Invalid phone format for {name}."
        else:
            record.add_phone(phone)
    return message


def show_all(book: AddressBook):
    if not book.data:
        print("Address book is empty.")
    else:
        for name, record in book.data.items():
            print(record)


@input_error
def change_phone(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = f"There is no contact {name}."

    if record is not None:
        if record.phones:
            original_phone = str(record.phones[0])
            record.remove_phone()
            record.add_phone(phone)
            message = f"Phone changed from {original_phone} to {phone}."
        else:
            message = "No phone number to change for this contact."

    return message

@input_error
def show_phone(args, book: AddressBook):
    name,  *_ = args
    record = book.find(name)
    message = f"There is no contact {name}."
    if record is not None:
        message = str(record.phones[0])
    return message

@input_error
def show_birthday(args, book: AddressBook):
    name,  *_ = args
    record = book.find(name)
    message = f"There is no contact {name}."
    if record is not None:
        message = str(record.birthday)
    return message

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    message = f"There is no contact {name}."
    if record is not None:
        record.add_bir(birthday)
        message = "Birthday added."
        if record.birthday.value is None:
            message = f"Birthday not added. Invalid date format for {name}."
    return message



def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            show_all(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(book.get_upcoming_birthdays())

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

