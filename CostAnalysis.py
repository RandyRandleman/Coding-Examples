#!/usr/bin/python
#Script is meant to help with Cost Savings between what MDT and its vendors
#Version 1.3
#Python 2.7
#Created By: Tony Knutson, Sr. Princ. Technologist Forensic Investigator anthony.r.knutson@medtronic.com

import time;
import os
import progressbar
import hashlib
from pyfiglet import Figlet
from sys import argv

#Opening Stuff
fig1 = Figlet(font='doom')
fig2 = Figlet(font='binary')
print fig1.renderText("ACME COMPANY")
print fig2.renderText("Version 2.0")
print("Last Updated 8 Jan 17" + "\n")
print ("COMPANY INFORMATION!" + "\n")
print ("\n" + "You are going to do a Cost Analysis for your cases")
print ("For questions regarding this script, Google-Foo" + "\n")
raw_input("Press Enter to Continue, have your numbers ready.....")

bar = progressbar.ProgressBar()
for i in bar(range(100)):
	time.sleep(0.02)

print("\n")
file_path = input("Specify the file path to log information")
print ("Opening your file....\n")
target = open(file_path, 'a')

m1 = raw_input("What is the level of classification?:   ")
target.write(m1 +   "\n")

#We need to put in information related to the case
target.write("Case Number:         " + "\n")
c1 = raw_input("What is the Case Number?:  ")
target.write(c1 + "\n")

#Time is going to matter when this is ran, in the event a future script is created
#For the purpose of appending when a case goes longer than expected
localtime = time.asctime( time.localtime(time.time()) )
print localtime
target.write(localtime + "\n")

#Don't change anything to this unless you finally learn how to do loops
print ("Time to enter all the fun information:      " + "\n")

target.write("How large of email pst was analyzed? \n")
email = raw_input("How big was the email dump?: ")
target.write(email + "\n")
email = int(email)

target.write("How many devices were imaged? \n")
acquisition_imaging = raw_input("How many devices were imaged?: ")
target.write(acquisition_imaging + "\n")
acquisition_imaging = int(acquisition_imaging)

target.write("How many hours did you spend analyzing? \n")
analysis_hours = raw_input("How many hours did you spend analyzing?: ")
target.write(analysis_hours + "\n")
analysis_hours = int(analysis_hours)

target.write("How many mobile apps were analyzed? \n")
acquisition_mobile = raw_input("how many mobile apps were analyzed?:  ")
target.write(acquisition_mobile + "\n")
acquisition_mobile = int(acquisition_mobile)

target.write("How many hours were spent consulting? \n")
consulting_hours = raw_input("How many hours were spent consulting: ")
target.write(consulting_hours + "\n")
consulting_hours = int(consulting_hours)

target.write("How large were the reports in GB? \n")
reporting = raw_input("How large were the reports in GB?: ")
target.write(reporting + "\n")
reporting = int(reporting)

target.write("Drives Needing to be wiped? \n")
additional_items = raw_input("Did you need to wipe any drives at all? Or would a vendor need to?: ")
target.write(additional_items + "\n")
additional_items = int(additional_items)

#This is where the magic happens
def vendor_costs(consulting_hours, analysis_hours, consulting_rate, analysis_rate, acquisition_rate, mobile_rate, additional_rate, email_rate, reporting_rate):
	return (consulting_hours*consulting_rate) + (analysis_hours*analysis_rate) + (acquisition_imaging*acquisition_rate) + (acquisition_mobile*mobile_rate) + (additional_items*additional_rate) + (email + email_rate) + (reporting + reporting_rate)

companies = {'CompanyA': {'consulting_rate': 400, 'analysis_rate': 300, 'acquisition_rate': 500, 'mobile_rate': 0, 'additional_rate': 200, 'email_rate': 0, 'reporting_rate': 15},
'CompanyB': {'consulting_rate': 295, 'analysis_rate': 275, 'acquisition_rate': 385, 'mobile_rate': 275, 'additional_rate': 500, 'email_rate': 165, 'reporting_rate': 5},
'CompanyC': {'consulting_rate': 295, 'analysis_rate': 295, 'acquisition_rate': 0, 'mobile_rate': 0, 'additional_rate': 0, 'email_rate': 0, 'reporting_rate': 0},
'CompanyD': {'consulting_rate': 525, 'analysis_rate': 425, 'acquisition_rate': 500, 'mobile_rate': 300, 'additional_rate': 25, 'email_rate': 250, 'reporting_rate': 90}}

for company, information in companies.items():
	estimated_cost = vendor_costs(consulting_hours, analysis_hours, information['consulting_rate'], information['analysis_rate'], information['acquisition_rate'], information['mobile_rate'], information['additional_rate'], information['email_rate'], information['reporting_rate'])
	print 'Estimated Cost for {} is {}'.format(company,estimated_cost)
	target.write('Estimated Cost for {} is {} \n'.format(company,estimated_cost))

# Adding Travel Information
target.write("\n")

print ("You are now entering information pertaining to your travel")

airfare = raw_input("what was airfare?:    ")
hotel = raw_input("What was hotel?:    ")
rental = raw_input("what was the rental?:   ")
expenses = raw_input("What was expenses?:   ")

airfare = int(airfare)
hotel = int(hotel)
rental = int(rental)
expenses = int(expenses)

total_cost = airfare + hotel+ rental + expenses
total_cost = int(total_cost)

print total_cost
target.write("Total cost for travel is:      \n")
target.write(str(total_cost))

#This was a pain in the ass, don't change it unless you figure out what to do with 
#the "No" statements
yesChoice = ['yes', 'y']
noChoice = ['no', 'n']
input = raw_input("Are you finished with this Cost Analysis?>  ").lower()

if input in yesChoice:
	#call method
	exit
elif input in noChoice:
	#exit game
	exit
else:
	print "Invalid Input"
	exit 


fig3 = Figlet(font='morse')
print fig3.renderText("Closing Case. Have a good day Tony!")

target.write("\n")
target.write("\n")
target.write(m1)

target.close()

hasher = hashlib.md5()
with open(file_path, 'rb') as afile:
	buf = afile.read()
	hasher.update(buf)
print(hasher.hexdigest())
