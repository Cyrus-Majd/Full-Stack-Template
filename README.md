# Full-Stack-Template
A template you can use later if you ever need to implement some full stack thing on the fly. An HTML form sends data to a backend.py running flask. The data is stored in a queue. A MySQL_Connector.py pops from the queue every time new data is added and ships it off to a MySQL server. To change details about the server, edit the parameters in MySQL_Connector.py's main method. Currently the database name (form_results) and table (login) to write to are hard coded. Further documentation might be provided depending on how lazy I am.
