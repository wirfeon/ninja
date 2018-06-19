#!/bin/bash

P=/www/ninja
BUILD=0
S=$PWD

diff $P/bot.py bot.py > /dev/null || sudo cp bot.py $P/

diff $P/Pipfile Pipfile > /dev/null || (sudo cp Pipfile $P/ && BUILD=1)
diff $P/Pipfile.lock Pipfile.lock > /dev/null || (sudo cp Pipfile.lock $P/ && BUILD=1)

if [ $BUILD == 1 ]; then
    cd $P
    sudo env PIPENV_VENV_IN_PROJECT=1 pipenv install --three
    sudo env PIPENV_VENV_IN_PROJECT=1 pipenv update
    cd $S
fi

diff $P/service service > /dev/null || (sudo cp service $P/ && sudo systemctl daemon-reload)

sudo systemctl restart bot.ninja
sudo systemctl status bot.ninja
