docker exec -it vmware-mongo sh
user wekan
show dbs
docker run -e DEST_HOSTNAME=postgres-db -e DEST_PORT=5432 -e DEST_DB=postgres -e DEST_ID=root -e DEST_PASSWORD=VMware1!  --network=vmware-network --name test mtl:1.0