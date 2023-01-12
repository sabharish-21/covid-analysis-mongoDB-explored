<br>
<center><h1><b>19AIE304 - BDMS END SEM PROJECT<br><br>Team - 03</b></h1></center>   
<br>

# <b>Team Members :</b>

<table>
  <tr>
    <th>Name :</th>
    <th>Roll No :</th>
  </tr>
  <tr>
    <td> Haripranav J M</td>
    <td>CB.EN.U4AIE20021</td>
  </tr>
  <tr>
    <td>Pravin Raj A K</td>
    <td> CB.EN.U4AIE20054</td>
  </tr>
    <tr>
    <td>Sabharish A L</td>
    <td>CB.EN.U4AIE20061</td>
  </tr>
    <tr>
    <td>Sai Sangavi C</td>
    <td>CB.EN.U4AIE20063</td>
  </tr>
    <tr>
    <td>Saivarsha R </td>
    <td>CB.EN.U4AIE20064</td>
  </tr>
</table>
<br>

# <b>Project Title : </b>
## Covid-19 Vaccination and Cases Analysis Along with 
## &emsp;&emsp;-> 3 Tier Architecture
## &emsp;&emsp;-> Data Replication [ CAP Theorem ]
## &emsp;&emsp;-> Data Streaming

<br>

# <b>File Contents :</b>

* > **Server** directory containing codes for the application server 
* > *data/country_vaccinations.csv* -> Dataset of global vaccination report  
* > *data/district_level_latest.csv* -> Dataset of Indian District vise Covid Cases
* > *`dataInsertion.py`* ->   Code for inserting data into the mongoDB database server
* > *`dataAnalysis.py`* &ensp;-> Code performing some analysis from the database

<br>

# <b>Instructions :</b>

> * For creating a _**mongodb**_ database with replication enabled, In the terminal type : <br><br>
&emsp; `mongod --dbpath <path_to_db_storage> --replSet <replication_set_name> --bind_ip <your_system_ip> ` <br> <br>
The same command can be given to all the different nodes provided they are in the same network

> * Next in the primary node open a terminal and then type <br><br> 
&emsp;`mongosh --host <your_system_ip>` <br><br>
Then in the mongosh shell to initiate the replication set and add the nodes<br><br> &emsp;`rs.initiate()`<br>&emsp;`rs.add(<node1_ip>:<port>)`<br>&emsp;`rs.add(<node2_ip>:<port>)` <br><br>
You can check the status of the database using <br><br> &emsp; `rs.status()`

> * Now we can have the mongoDB url for connecting through a application
<br><br>&emsp;`mongodb://<node1_ip>:<node1_port>,<node2_ip>:<node2_port>,<node3_ip>:<node3_port>/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.0` <br> <br>
Once you get the URL make sure you also change it in the _**Server/mongoDB/views.py**_ `connString` variable

<br>

# <b> Applciation Server : </b>

The application server is developed using Python's Django Framework. <br>
To start the server run the following command in the terminal at the **Server** directory: <br>
> `python manage.py runserver` <br>

To access the application server in the network run the following command in the terminal at the same directory <br>
> `python manage.py runserver 0.0.0.0:<port>` <br>  [or] <br>
`python manage.py runserver <system_ip>:<port>`

To create a new admin account to access the server run the following command:<br>
> `python manage.py createsuperuser` <br>

and fill the asked details and then make sure you enter the same in the admin dashboard and the datainsertion code <br> <br>
Sample username and password : <br>
<b>User Name : </b> admin <br>
<b>Password : </b> admin
<br>
<br>

# <b>Images : </b>

![Login Page](./images/login.png)
![Dashboard Page](./images/dashboard.png)
![Analysis Page](./images/analysis.png)
![Edit Data Page](./images/editdata.png)


## Analysis Images

![Analysis One](./images/analysis1.png) ![Analysis Two](./images/analysis2.png) 
<img class=mobile-image src="" />
<img class=mobile-image src="images\analysis4.png" />
<img class=mobile-image src="images\analysis2.png" />
<img class=mobile-image src="images\analysis5.png" />
<img class=mobile-image src="images\analysis3.png" />
