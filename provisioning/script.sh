docker exec -it vmware-mongo sh
user wekan
mongorestore --host 127.0.0.1:27017 -u root -p VMware1! --authenticationDatabase admin -d wekan ../wekan