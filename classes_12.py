from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
import pickle

class BirthdayError(Exception):
    ...


class Field:
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")


class Birthday(Field):
    def __init___(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            # raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
            raise BirthdayError()


class Record:
    def __init__(
        self, name: Name, phone: Phone = None, birthday: Birthday = None
    ) -> None:
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.add_phone(phone)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = datetime(
            today.year, self.birthday.value.month, self.birthday.value.day
        )
        if next_birthday < today:  # якщо день народження вже був у поточному році
            next_birthday = datetime(
                today.year + 1, self.birthday.month, self.birthday.day
            )
        days_left = (next_birthday - today).days
        return days_left

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
        for idx, p in enumerate(self.phones):
            if p.value == phone.value:
                return (
                    f"Phone:{self.phones.pop(idx)} - was remove in contact {self.name}"
                )

    def __str__(self) -> str:
        phones = "; ".join(str(p) for p in self.phones) if self.phones else "not added"
        return f"Contact name - {self.name}, contact phones - {phones}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, phone={self.phones}, birthday={self.birthday})"


# emp = Record("Jill", birthday=Birthday("1995-07-30"))
# print(emp.birthday.value)
# print(emp.days_to_birthday())


class AddressBook(UserDict):
    def __iter__(self, n=1):
        self._index = 0
        self._items = list(self.data.values())
        self._step = n
        return self

    def __next__(self):
        if self._index < len(self._items):
            item = self._items[self._index]
            self._index += self._step
            return item
        else:
            raise StopIteration

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} added successfully"
    
    def save_to_file(self, file_path):
        with open (file_path, "wb") as fh:
            pickle.dump(self.data, fh)
    def load_from_file(self, file_path):
        try:
            with open (file_path, "rb") as fh:
                data = pickle.load(fh)
                self.data.update(data)
            return True
        except:
            return False


    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
