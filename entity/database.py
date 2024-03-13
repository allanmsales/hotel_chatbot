class Database:
    def __init__(self, data):
        self.data = data

    def save_data(self):
        print(f'Reservation Saved in Database: {self.data}')