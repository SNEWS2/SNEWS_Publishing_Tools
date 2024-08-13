
# FAQ and Troubleshooting

We try to collect the common questions and issues that users have when using the SNEWS Publishing Tool. 
If you have a question that is not answered here, please feel free to open an issue on the [GitHub repository](https://github.com/SNEWS2/SNEWS_Publishing_Tools)

## How do I set up my hop credentials?

Easiest is to follow the instructions in the [Quick Start](https://snews-publishing-tools.readthedocs.io/en/latest/user/quickstart.html) guide. <br>
Once created you can add your credentials from the terminal
    
    ```bash
    hop auth add
    ```
which will prompt you to enter your username and password. Then your credentials will be stored on your local machine (`hop auth locate`).
You do not need to do anything else, as snews_pt will automatically use these credentials when you publish or subscribe to the SNEWS servers.

## How do I know if I have the correct permissions to publish or subscribe to the SNEWS servers?
During development and in the actual production environment, you will need to have the correct permissions to publish or subscribe to the SNEWS servers.
The permissions are given for certain topics within certain groups. Simply go to [https://my.hop.scimma.org/hopauth/](https://my.hop.scimma.org/hopauth/) and check if you are in snews group.
If so, check which topics you have access to. The topics are explained in [hopskotch page](./hopskotch.md). If you are not in the snews user groups, request to be added by sending a message on SNEWS slack, on the implementation channel.

## Kafka Errors
There can be many reasons for Kafka errors. The most common ones are;
 ### Network is unreachable
If your network is not reachable, you will get an error message like this;
```bash
%3|1723572803.484|FAIL|rdkafka#consumer-2| [thrd:sasl_ssl://kafka.scimma.org:9092/bootstrap]: sasl_ssl://kafka.scimma.org:9092/bootstrap: Failed to connect to broker at [ns-137.awsdns-17.com]:9092: Network is unreachable (after 20ms in state CONNECT)
...
cimpl.KafkaException: KafkaError{code=_TRANSPORT,val=-195,str="Failed to get metadata: Local: Broker transport failure"}
```
Try using a different network to confirm if the issue is with your network. Sometimes, the network you are using might have a firewall that blocks the connection to the Kafka server.



