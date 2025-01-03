# Multiband Astronomical Reduction

MAR (Multiband Astronomical Reduction) is a comprehensive and adaptable data reduction package designed to process data from the Southern Photometric Local Universe Survey (S-PLUS). It includes a Python package, a server, a frontend, and a database. MAR utilizes external packages such as Sextractor, Scamp, Swarp, and IRAF for certain operations.

MAR was also developed to be an open source code so that it could potentially help others.

To facilitate ease of use, we have integrated MAR into Docker containers that work in conjunction with one another. One container is dedicated to the MAR-frontend, which compiles the React.JS code (website). Another container is responsible for the marServer, which compiles all dependencies, the MAR Python package, and runs the server. The final container is for the nginx proxy server, which handles all routing tasks.
Docker configs for each container: 

- MAR-frontend (/MAR-frontend/Dockerfile)
- marServer (/Dockerfile)
- Nginx (/docker-compose.yml)

To install Docker-Compose you need to have docker installed ([docker on ubuntu](https://docs.docker.com/engine/install/ubuntu/)), then just download docker compose [from their GitHub](https://github.com/docker/compose/releases).

*A tip is to download the executable, run **"sudo chmod +x {executable}"** on it and then copy it to something like /usr/bin/docker-compose to call it from anywhere as "docker-compose".*

---

#### mar (python package)

The mar python package contains all essential functions to perform the reduction. (overscan, prescan, trim, masterbias, masterflats, fringe, and all third party softwares wrappers also like Sextractor, Scamp, Swarp and so on...).

#### [Here](docs/mar_python.md) is a more detailed document explaining the functions and classes. 

---

#### marServer API 

The server was developed to make a easy and remote pipeline with almost self explanatory functions and so almost anyone may be able to reduce data. 

#### [Here](docs/API.md) is a further intro to the API of the server.
#### [Here](docs/database.md) is a further description on the tables generated by the pipeline. 

---

#### MAR-frontend 

The frontend developed using ReactJS is a interface made from the marServer API, it features a calendar to facilitate the time series data visualization and also other tools to search on the db, search for images, reduce, flag, invalidade images, scan. Almost every marServer API feature is implemented in the MAR-frontend.

---

### Steps to build and run the containers.

Firstly, you need to have PostgreSQL 12 or higher installed (good way to install postgresql is described here https://devopscube.com/install-postgresql-on-ubuntu/) and configured to accept remote connections. This can be done on either your local machine or a remote server. For instructions on how to enable remote access, please refer to this link: https://stackoverflow.com/questions/18580066/how-to-allow-remote-access-to-postgresql-database.

### Database

MAR was developed to work with PostgreSQL 12+, although other relational databases may also work.

It is not recommended to use PostgreSQL in a Docker container with a short data life cycle for production environments.

When configuring your PostgreSQL (psql), you may run the following default settings for MAR. The server container will attempt to connect to the host machine. You may change this if you are using a different setting.

```SQL
CREATE DATABASE mar;
ALTER USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE mar TO postgres;
```

#### If you dont want to install postgres 

Just use it at a docker container. Change **"172.17.0.1"** from marServer/marServer/settings.py variable DATABASE.HOST to **"db"** and comment out these lines at "docker-compose.yml":

```
extra_hosts:
     - "host.docker.internal:172.17.0.1"
```

and:

```
db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
```

and:

```
depends_on:
    - db
```

**Note!** Using postgres in docker should lead into loss of data once container is "relaunched".

--- // ---

### Setting up datafolder

A folder named "reductionmedia" should be created at the root of this repository. This folder will serve as the data folder, where all raw images and products will be stored. 

Another folder named "martmp" should also be created to store all temporary files. 

It is recommended to create symlinks for both folders. Perhaps the origin folder of the symlink for "reductionmedia" should be located in a large storage space, while "martmp" is best stored on an SSD or similar device that allows for fast IO operations.

### Instalation

Now that the data folder is set up and the database is ready, we are good to proceed. Navigate to the root of the repository and execute the following command:

```bash
sudo docker-compose build
```

Then run the following to populate the database and create a user (this may need sudo permission):
  
```bash
sudo docker-compose run --rm server python3.11 manage.py migrate

sudo docker-compose run --rm server python3.11 manage.py createsuperuser
```

Finally run this to get the container up and running:

```bash
sudo docker-compose up
```

Copy the raw images to the "reductionmedia" folder. One suggestion to maintain file organization is to create a folder named "MYFOLDER" inside the "reductionmedia" directory and copy all files there.

#### The MAR frontend can be accessed from 127.0.0.1:3001

<br/>
<br/>

### Pipeline outputs

These folders are created inside the reductionmedia folder, and are used by the pipeline to save intermediary and final products of the reduction. 

| Folder Name   | Type                                                                                      |
|---------------|-------------------------------------------------------------------------------------------|
| MASTERS       | masterflats, masterbias and fringe frames are stored.                                      |
| PROCESSED     | processed science images (wt coadding) will be stored.                                        |
| SCAMP         | Scamp output (astrometry)                                                                 |
| SEXTRACTOR    | Sextractor output                                                                         |
| SWARP         | Swarp output (config files) **                                                            |
| THUMBS        | Thumbs and plots of all images. *                                                         |
| TILES         | Coadded Tiles. Final Product. **                                                          |
| TMP ~~unused~~ | Some test files are added here |


Please cite:

```
@article{SCHWARZ2025100899,
title = {MAR: A Multiband Astronomical Reduction package},
journal = {Astronomy and Computing},
volume = {51},
pages = {100899},
year = {2025},
issn = {2213-1337},
doi = {https://doi.org/10.1016/j.ascom.2024.100899},
url = {https://www.sciencedirect.com/science/article/pii/S2213133724001148},
author = {G.B. Oliveira Schwarz and F. Herpich and F. Almeida-Fernandes and L. Nakazono and N.M. Cardoso and E. Machado-Pereira and W. Schoenell and H.D. Perottoni and K. Menéndez-Delmestre and L. Sodré and A. Kanaan and T. Ribeiro},
keywords = {Astronomical, Image, Multiband, Reduction, Pipeline, Software},
abstract = {The Multiband Astronomical Reduction (MAR) is a multithreaded data reduction pipeline designed to handle raw astronomical images from the Southern Photometric Local Universe Survey, transforming them into frames that are ready for source extraction, photometry and flux calibration. MAR is a complete software written almost entirely in Python, with a flexible object-oriented approach, simplifying the implementation of new moduli. It contains a Python package, mar, with all essential operations to be used, a server where the pipeline resides, an interface that allows users to navigate quickly, and a database to store all data as well as important information and procedures applied to the images. MAR is now regularly used to process data from the Southern Photometric Local Universe Survey, but its methods may be used for developing other multiband data reduction packages. This paper explains each pipeline modulus of MAR and describes how its routines work.}
}
```


