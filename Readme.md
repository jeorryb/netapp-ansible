# ansible-netapp
Ansible modules and playbooks utilizing the Python API in the NetApp Manageability SDK

This utilizes custom Ansible modules built using the NetApp Manageability SDK (NMSDK). The playbooks aid in the provisioning and management of Clustered Data ONTAP and hopefully entire FlexPods.

## Dependencies

Install the NetApp Manageability SDK

https://community.netapp.com/t5/Software-Development-Kit-SDK-and-API-Discussions/NetApp-Manageability-NM-SDK-5-4-Introduction-and-Download-Information/td-p/108181

!!!Make sure to add the location of the NMSDK to your PYTHONPATH environment variable!!!

e.g.

PYTHONPATH="/Volumes/data/Netapp/netapp-manageability-sdk-5.5/lib/python/NetApp:$PYTHONPATH"

export PYTHONPATH

## Getting Started
I've provided a Dockerfile in the repository to make it easier to get started with Ansible and the NetApp Manageability SDK.
After installing Docker and downloading the NMSDK, run the following command from the same directory where you downloaded the nmsdk zip file.

```shell
docker build -t <image name> .
```

Once you've downloaded the ssl cert for the cluster, (See [here](http://www.datarambler.com/devops-batteries-included/) for a more in-depth explanation for this.) run the following command to execute your playbook as a one-liner.

```shell
docker run -it -v <local ssl cert location>:/etc/ssl/certs -v <local dir for your playbook>:/ansible/playbooks <image name> <playbook name>
```

### Example

```shell
docker run -it -v $(pwd):/etc/ssl/certs -v /Users/jeorryb/images/ansible_nmsdk:/ansible/playbooks ansible-nmsdk nmsdk.yaml

```
