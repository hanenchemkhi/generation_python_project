#!/usr/bin/env python
import csv
import json
from re import sub
import pandas as pd

"""Calculates the salary of an employee."""   
def calculate_salary(rate, hours):
    rate_value = float(sub(r'[^\d.]', '', rate))
    if hours <= 40 :
        regular_pay = hours * rate_value
        ot_pay = 0.0
        gross_pay = regular_pay
        fed_tax = gross_pay * 0.1
        state_tax = gross_pay * 0.06
        fica = gross_pay * 0.03
        net_pay =   gross_pay - (fed_tax+ state_tax+ fica)
        return regular_pay,ot_pay,gross_pay, fed_tax, state_tax, fica, net_pay

    regular_pay = 40 * rate_value 
    ot_pay = (hours - 40)* rate_value * 1.5 
    gross_pay = regular_pay + regular_pay
    fed_tax = gross_pay * 0.1
    state_tax = gross_pay * 0.06
    fica = gross_pay * 0.03
    net_pay =   gross_pay - (fed_tax+ state_tax+ fica)
    return regular_pay,ot_pay,gross_pay, fed_tax, state_tax, fica, net_pay
    
"""Appends a record of an employee to a JSON file"""
def save_payroll(employee_info, salary):
    employee_dic = {"Employee Name": employee_info[0],\
                        "Hours Worked": employee_info[1], \
                        "Pay Rate": employee_info[2], \
                        "Regular Pay": "${:.2f}".format(salary[0]), \
                        "OT Pay" : "${:.2f}".format(salary[1]), \
                        "Gross Pay": "${:.2f}".format(salary[2]), \
                        "Fed Tax" : "${:.2f}".format(salary[3]), \
                        "State Tax": "${:.2f}".format(salary[4]), \
                        "FICA": "${:.2f}".format(salary[5]),\
                        "Net Pay": "${:.2f}".format(salary[6])}
    with open ("payroll.json", "r+") as json_file :
        data_file = json.load(json_file)
        data_file.append(employee_dic)
        # Moves the cursur to the beginning of the file object in order to add the new list. 
        json_file.seek(0) 
        json.dump(data_file, json_file, indent = 4) 

"""For readability, we will convert the JSON file holding the payroll to EXCEL file.
"""
def transfer_json_to_excel():
    with open("payroll.json", "r") as json_file:
        payroll_data = json.loads(json_file.read()) # Reads and loads the payroll data 
        df = pd.DataFrame(payroll_data) # Converts the data to a data frame 
        df.to_excel('pyroll_xls.xlsx') # Saves the data to an EXCEL file

"""
Setting up the payroll file in  Json format where all employee records will be stored.
"""
with open("payroll.json", "w") as file :
    file.write("[]")

"""Calculate salary of all employees"""
with open("employee.csv", "r") as emp_info : # Reads employee data from a CSV file 
    csv_reader = csv.reader(emp_info) 
    next(csv_reader) #skip the header
    for employee in csv_reader : 
        """For every employee in the list, we will calculate their pay and save it to JSON file"""
        salary = calculate_salary(employee[1], float(employee[2])) 
        save_payroll(employee, salary)
"""
For readability, we will convert the JSON file holding the payroll to EXCEL file
"""
transfer_json_to_excel()
