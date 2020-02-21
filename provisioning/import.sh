#! /bin/bash
mongorestore --host mongo-db --db wekan --collection census --type json --file /mongo-seed/census.json --jsonArray