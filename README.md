# MyPortfolio
Design a graph to manage you stock investment in NSE

![image](https://github.com/user-attachments/assets/7aa68cf9-5887-49f1-9e9c-d69c7f434479)
Can do very basic analysis with this..

### How it works
It uses python libraries like Numpy, Pandas to read investment data from excel,
map it with historical price change from Yahoo finance via data scrapping
and finally plots the graph using matplotlib

## Steps
Install requirements.txt (better use a virtaul env)
Download you PL stock report from Groww. Rename & replace it to rpt.xlsx. Sample is given, maintain the exact column names and structures.
Update config.py file; for first run keep stock history generation = 1; make it 0 to skip web data scrapping.
You should see the graph in few minutes :)


### Failures
In case yahoo website gets updated with new table/class/attribute names; need to update the code accordingly
Sometimes few stock might fail to fetch history; retry or downlaod data manually.

Suugestions are accepted... Thank you!!!
