Regular Expression Exercise

TASK 1:
The text file WN24_dates.txt contains 500 lines, such that each line corresponds to a medical note. Each line in the given file has a date that needs to be extracted. Once you have extracted the dates, normalize them according to the following rules:

Assume all dates in xx/xx/xx format are mm/dd/yy.
Assume dates in xx/xx format are mm/yy.
Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
Each date should be normalized to the yyyy-mm-dd format.

TASK 2: 
After getting the normalized date, you are supposed to push all dates by a specific number of days (let's say 40 days in this task). Specifically, assuming you get a date 2000-01-01 in TASK 1, you are supposed to return 2000-02-10 in TASK 2. 

