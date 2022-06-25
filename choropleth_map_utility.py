



from enum import Enum

# the kinds of data the app provides
class Illness(Enum):
    Covid_19 = ''

    # Backyard Poultry
    BP_Salmonella = 'https://www.cdc.gov/salmonella/backyardpoultry-06-22/files/Where-Sick-People-Lived.xlsx' 

    # Peanut Butter
    PB_Salmonella = '' 

    Monkey_Pox = ''

# vars we need
# file_type, column_state, column_mainvalue, legend_name, date_posted
class Parameters():
    def __init__(self, i, ft, cs, cm, ln, dp):
        self.illness_type = i # Illness 
        self.file_type = ft
        self.column_state = cs
        self.column_mainvalue = cm
        self.legend_name = ln
        self.date_posted = dp

# hard coded parameters. received from website
parameters = {
    Illness.Covid_19 : Parameters(Illness.Covid_19, "CSV", "state", "new_case", "New Covid-19 Cases", "June 25 2022"),
    Illness.BP_Salmonella : Parameters(Illness.BP_Salmonella, "XLSX", "State of Residence", "Number of Sick People", "Backyard Poultry Salmonella", "June 9 2022"),
    Illness.PB_Salmonella : Parameters(Illness.PB_Salmonella, "XLSX", "State of Residence", "Number of Sick People", "Peanut Butter Salmonella", "May 26 2022"),
    Illness.Monkey_Pox : Parameters(Illness.Monkey_Pox, "CSV", "State", "Cases", "Monkey Pox Cases", "June 24 2022")
}


