#!/bin/bash

P=/www/ninja
BUILD=0
S=$PWD

diff $P/bot.py bot.py || sudo cp bot.py $P/

diff $P/Pipfile Pipfile || (sudo cp Pipfile $P/ && BUILD=1)
diff $P/Pipfile.lock Pipfile.lock || (sudo cp Pipfile.lock $P/ && BUILD=1)

if [ $BUILD == 1 ]; then
    cd $P
    sudo env PIPENV_VENV_IN_PROJECT=1 pipenv install --three
    cd $S
fi

diff $P/service service || (sudo cp service $P/ && sudo systemctl daemon-reload)

sudo systemctl restart bot.ninja
sudo systemctl status bot.ninja
