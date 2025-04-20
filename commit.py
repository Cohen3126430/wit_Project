class Commit:
    def __init__(self, author, date, message):
        self.author = author
        self.date = date
        self.message = message


    def __str__(self):
       return f"Author: {self.author}\nDate: {self.date}Message: {self.message}"
