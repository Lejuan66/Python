# Cloud-Computing-Airfoil Team 11
Airfoil project

Steps to run it:

`install python-openstackclient`

`cd orchestration && ./spawn_master`

A master node gets spawned and prints its IPv6 address in the terminal. IPv6 is configured automatically, but a floating IPv4 address can be attached manually through the OpenStack interface. 

Visit this url with a master node IP and your favorite browser:
`<ip>:5000/airfoil`

Fill in the form and wait for the result to download. (Please be nice with parameters, we're not cleaning them.)

If you instead wish to receive the data into your command window. You can use the REST API with cURL:
`curl -o results.tar <ip>:5000/airfoil -d minA=int, -d maxA=int -d nrA=int -d nrN=int -d nrR=int -d NACA=str -d samp=int -d vi=float -d speed=float -d t=float`

The work can be monitored through Flower at this url:
`<ip>:5555`

