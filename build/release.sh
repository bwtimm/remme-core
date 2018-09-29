#!/bin/bash

IMAGES=$(docker images | grep -Po '(?<=remme\/)[a-z-]+(?=\s+latest)')
RELEASE_NUMBER=$(git describe --abbrev=0 --tags)

COMPOSE_DIR=./compose
RELEASE_DIR=./remme-core-$RELEASE_NUMBER-release
COMPOSE_RELEASE_DIR=$RELEASE_DIR/compose

./build/clean.sh
./build/build.sh

mkdir $RELEASE_DIR
mkdir $COMPOSE_RELEASE_DIR

cp $COMPOSE_DIR/base.yml ./$COMPOSE_RELEASE_DIR
cp $COMPOSE_DIR/genesis.yml ./$COMPOSE_RELEASE_DIR
cp -R config ./$RELEASE_DIR
cp ./scripts/run.sh ./$RELEASE_DIR

for IMAGE in $IMAGES; do
    docker tag remme/$IMAGE:latest remme/$IMAGE:$RELEASE_NUMBER
done

sed -i -e "s/:latest/:$RELEASE_NUMBER/g" $COMPOSE_RELEASE_DIR/*.yml
