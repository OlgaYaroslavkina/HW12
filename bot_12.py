from classes_12 import Name, Phone, Birthday, Record, AddressBook

address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено!"
        except ValueError:
            return "Неправильний формат вводу!"
        except IndexError:
            return "Неправильний формат команди!"

    return wrapper


@input_error
def add_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = None
    if len(args) == 3:
        birthday = Birthday(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    birthday = None
    if len(args) == 4:
        birthday = Birthday(args[3])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact with name {name} in address book"


@input_error
def remove_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.remove_phone(phone)
    # else:
    return f"No contact with name {name} in address book"


def unknown_command(*args):
    return "Введіть іншу команду"


def show_all_command(*args):
    if address_book.data:
        result = "Список контактів:\n"
        return result + "\n".join(str(r) for r in address_book.data.values())
    else:
        return "Список контактів порожній."


@input_error
def search_command(search_text: str):
    search_result = []
    # Перебираємо всі записи в адресній книзі
    for record in address_book.data.values():
        name_str = str(record.name)
        phone_str = ";".join(str(phone) for phone in record.phones)
        # ПеревіряємоБ чи міститься пошуковий текст у імені або номерах телефонів
        if search_text.lower() in name_str.lower() or search_text in phone_str:
            search_result.append(str(record))
    # Повертаємо результат пошуку або повідомлення про відсутність результатів
    if search_result:
        return "Результити пошуку:\n" + "\n".join(search_result)
    else:
        return "Пошук не дав результатів."


def hello_command(*args):
    return "How can I help you?"


def exit_command(*args):
    return "Good bye!"


COMMANDS = {
    hello_command: ("hello",),
    add_command: ("add", "+"),
    change_command: ("change", "зміни"),
    remove_command: ("remove",),
    show_all_command: ("show all",),
    search_command: ("search",),
    exit_command: ("good bye", "close", "exit"),
}


@input_error
def parser(text: str):
    for cmd, keywords in COMMANDS.items():
        for keyword in keywords:
            if text.lower().startswith(keyword):
                data = text[len(keyword) :].strip().split()
                return cmd, data
    # Додамо розпізнавання команди пошуку
    if text.lower().startswith("search"):
        data = text[len("search") :].strip()
        return search_command, [data]
    return unknown_command, []


def main():
    print("Вітаємо у боті-асистенті!")
    while True:
        user_input = input("Введіть команду: ")
        cmd, data = parser(user_input)
        result = cmd(*data)
        # print(result)
        if cmd == exit_command:
            # break
            address_book.save_to_file("address_book.pickle")
            print(result)
            break
        # result = cmd(*data)
        print(result)


if __name__ == "__main__":
    if address_book.load_from_file("address_book.pickle"):
        print("Адресну книгу відновлено з файлу")
    else:
        print("Створено нову адресну книгу")
    main()
