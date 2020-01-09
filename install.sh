#/usr/bin/env bash
virtualenv -p $(which python3) barleynet-env
source barleynet-env/bin/activate

pip install -U pip
pip install Flask redis scipy statsmodels

wget http://download.redis.io/releases/redis-4.0.14.tar.gz
tar xzf redis-4.0.14.tar.gz
cd redis-4.0.14
make
cp src/redis-server src/redis-cli ${VIRTUAL_ENV}/bin
cd ..