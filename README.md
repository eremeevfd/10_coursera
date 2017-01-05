# Coursera Dump

Thank you for using my script to gather course info from [coursera.org](www.coursera.org).

## Quick start
<pre>
$ pip install -r requirements.txt  
$ python3 coursera.py </pre>

## Script purpose

This script gets 20 random courses [here](https://www.coursera.org/sitemap~www~courses.xml).
Then gets their main info (if available), such as:  
* Course title
* Course language, including subtitles
* Date of start 
* Duration in weeks 
* Average rating
  
Finally, script saves all info to __.xlsx__ file, asking you a filepath.  
__*Be patient, http connections take some time.*__

## Typical output

Title | Language | Start date | Duration (weeks) | Average rating
--- | --- | --- | --- | ---
Seguridad agroalimentaria |	Spanish | 2017-01-09 |	4 |	4.6
Trading Basics | English |	2017-01-02 |	4 |	4.4
