# BarleyNet REST-like API

BarleyNet API is processed under [Flask](https://palletsprojects.com/p/flask/) (simple web framework) and [Redis](https://redis.io/) (in-memory data structure store).

## Requirement
- Redis 4 or higher
- Python 3.x
	- Python packages : Flask, redis, scipy, statsmodels


## Installation of API

### 1. Get API and data files
```bash
$ git clone https://github.com/netbiolab/BarleyNet
$ cd BarleyNet
```
### 2. Setup environment
You can use Anaconda (distribution of Python and R with simplifying managing their packages) or Python's virtualenv


### 2.1. Installation using `conda` (Anaconda or Miniconda)
Create an conda environment with installing packages
```bash
(base) $ conda create -n barleynet-env python=3 redis=4 flask redis-py scipy statsmodels -y
(base) $ conda activate barleynet-env
```
### 2.2. Installation using `virtualenv`
If you are not using `conda`, you may use `virtualenv` to create an environment and to install packages.
```bash
# for ubuntu linux
sudo apt install python3-virtualenv python3-dev
```
Run the commands below step-by-step or run `install.sh` file.

- Preparing an virtual environment
	```
	$ virtualenv -p $(which python3) barleynet-env
	```
- Installation of python packages from PyPI repository.
	```
	$ source barleynet-env/bin/activate
	(barleynet-env) $ pip install Flask redis scipy statsmodels
	```
- Installation of Redis
	- Compiling Redis
		```bash
		(barleynet-env) $ wget http://download.redis.io/releases/redis-4.0.14.tar.gz
		(barleynet-env) $ tar xzf redis-4.0.14.tar.gz
		(barleynet-env) $ cd redis-4.0.14
		(barleynet-env) $ make
		(barleynet-env) $ cp src/redis-server src/redis-cli ${VIRTUAL_ENV}/bin
		(barleynet-env) $ cd ..
		```
	- Or you can install Redis via package managers such as apt, yum, dnf.
		```bash
		# for Ubuntu or Debian linux
		$ sudo apt install redis-server
		```


## Running Redis 
```bash
(barleynet-env) $ cd data/redis
(barleynet-env) $ gunzip dump.rdb.gz
(barleynet-env) $ redis-server redis.conf
```
> Redis server will run on the default port 6379. You can change the port number in `redis.conf` file. 


## Running API
Open the git directory in another shell prompt.
```bash
(barleynet-env) cd barleynet-api
(barleynet-env) export FLASK_ENV=development    # run the Flask app in development mode
(barleynet-env) python wsgi.py
 * Serving Flask app "api" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 118-953-618

```
Now API is running.
> Check `REDIS_SERVER` variable on `config.py` if you changed the redis port number.

## Using API
The API help page is available in `http://127.0.0.1:5000/help`.
You can test it through API clients such as [Postman](https://www.getpostman.com).

## Citation
Lee, S. , Lee, T. , Yang, S. , and **Lee, I.** (2019). BarleyNet: a network-based functional omics analysis server for cultivated barley, *Hordeum vulgare L*. Manuscript submitted for publication.
