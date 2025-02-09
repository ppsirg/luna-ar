import os
import shelve
from threading import Lock
from contextlib import contextmanager
from icecream import ic


@contextmanager
def thread_safe_shelve(filename: str):
    lock = Lock()
    lock.acquire()
    with shelve.open(filename) as db:
        yield db
    lock.release()


class DataStorage:
    __instance = None
    __lock = Lock()
    filename = "datastorage.pickle"

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def wipe(cls):
        os.remove(cls.filename)

    def add(self, key: str, data_dict):
        """Add a new entry to the storage with the given key and dictionary."""
        with thread_safe_shelve(self.filename) as db:
            try:
                db[key] = data_dict
                return True
            except Exception as e:
                print(f"An error occurred while adding data: {e}")

    def get(self, key: str):
        with thread_safe_shelve(self.filename) as db:
            try:
                return db[key]
            except Exception as err:
                print(f"not found {err}")
                return None

    def delete(self, key: str):
        """Delete an entry from the storage using the given key."""
        with thread_safe_shelve(self.filename) as db:
            try:
                del db[key]
                return True
            except KeyError:
                print("Key does not exist in the database.")
                return True
            except Exception as e:
                print(f"An error occurred while deleting data: {e}")
                return None

    def update(self, key: str, data_dict):
        """Update an existing entry in the storage with a new dictionary."""
        with thread_safe_shelve(self.filename) as db:
            try:
                if key in db:
                    db[key] = data_dict
                    return True
                else:
                    print("Key does not exist in the database.")
                    return False
            except Exception as e:
                print(f"An error occurred while updating data: {e}")
                return None

    def list(self):
        """List all keys and their associated dictionaries."""
        with thread_safe_shelve(self.filename) as db:
            try:
                return [{"key": k, "value": v} for k, v in db.items()]
            except Exception as e:
                print(f"An error occurred while listing data: {e}")
                return None
