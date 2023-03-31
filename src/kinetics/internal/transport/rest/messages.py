from enum import Enum


class Message(Enum):
    TABLE_PARAMETERS_NOT_FOUND = "Table parameters not found in db"
    TABLE_PARAMETERS_NOT_CREATED = "Table parameters not saved in db"
    SOLUTION_DATA_NOT_FOUND = "Solution data not found in db"
    INPUT_DATA_NOT_FOUND = "Input data not found in db"
    INPUT_DATA_NOT_CREATED = "Input data not saved in db"
