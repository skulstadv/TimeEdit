# TimeEdit
Automatic room reservation script for HIG time-edit website

# Outdated, NTNU switched system used for reservations. See https://github.com/skulstadv/NTNU-Roomshark for updated version.
Room numbers would have to be updated to use this script in other places than HiG.
Same goes for URL used with selenium and requests. 

##To grab selenium URL:
  * Log in to where you make reservations, delete the TEwebhigdb1 cookie
  * F5, copy the URL "Student" points to. Use this for selenium.

##To grab room numbers and URL for making reservation:
  * Log in, choose time, date and room. Fill the required fields.
  * F12 -> Network and copy the xhr request as curl for instance. Your room ID should be in the 'o' field.
  * Make sure you copy the URL from the xhr request aswell and use it for the post request.
