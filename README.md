# Requirement
Make sure to have python3 installed
## Ubuntu Environment 
```
sudo apt-get install python3.6 python3-pip libmariadbclient-dev
pip3 install -r requirements.txt
pip3 install mysql-connector-python
```
## CentOS Environment
```
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
sudo yum update
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
sudo yum install mariadb-devel
pip3 install -r requirements.txt
pip3 install mysql-connector-python
```
# Running the code
```
python3 manage.py
```