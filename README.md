net-tester
============
Python3.x based client/server application for testing a network connection between endpoints.

The server supports concurrency so multiple clients can be connected to it at the same time.

### Usage:

```$ git clone https://github.com/JosephDix/net-tester.git```

Run `$ python server.py` on a machine connected to one endpoint.

Edit `client.py` so that `SRV_IP` is equal to an accessible ip of server.py

Run `$ python client.py` on other endpoint.


### Example:
![client example](https://raw.githubusercontent.com/JosephDix/net-tester/master/images/Example.png "client example")