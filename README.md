# M2P-ETL
Mongo to Postgres ETL

## Getting started
### Prerequisites
- Docker version 19.03.5, build 633a0ea
- Python 3.8.1

### Start mongo and postgres
#### Docker-Compose 
```shell script
docker-compose -f ./provisioning/docker-compose.yml up -d
```

#### Docker command
**Mongo Database**
```shell script
docker pull mongo:4.2.2
docker run -d -p 27017:27017 -v /opt/mongo/data/configdb:/data/configdb -v /opt/mongo/data/db:/data/db --name mongodb mongo:4.2.2
```

**Postgres Database**
```shell script
docker pull postgres:12.2
docker run -d -p 5432:5432 -v /opt/postgresqk/var/lib/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=VMware1! --name postgresql postgres:12.2```
```

#### Pylint 
- source-code, bug and quality checker for the Python programming language
```shell script
python lint.py --path ../M2P-ETL --threshold 5
```

#### Docker build
```shell script
docker build -t [name]:[version-number] .
```

## Requirements
- astroid==2.3.3
- isort==4.3.21
- lazy-object-proxy==1.4.3
- mccabe==0.6.1
- numpy==1.18.1
- pandas==1.0.1
- psycopg2-binary==2.8.4
- pylint==2.4.4
- pymongo==3.10.1
- python-dateutil==2.8.1
- pytz==2019.3
- six==1.14.0
- SQLAlchemy==1.3.13
- wrapt==1.11.2

