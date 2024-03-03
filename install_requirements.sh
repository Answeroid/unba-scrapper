#!/bin/bash

while true; do
  read -r -p "\nDo you want to install requirements.txt together with virtual environment? [Yy/Nn]: " yn
  case $yn in
    [Yy]* ) echo Installing...; exit;;
    [Nn]* ) echo Exiting...; exit;;
    * ) echo "Please respond correctly.";;
  esac
done

# Check that python3 is installed
command -v python3 >/dev/null 2>&1 && echo Python 3 is installed

# Check that python installed
command -v python >/dev/null 2>&1 && echo Python is installed

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    MSYS_NT*)   machine=Git;;
    *)          machine="UNKNOWN:${unameOut}"
esac

echo "Running on ${machine}..."

echo "Installing virtualenv on host..."
if [[ "$machine" == MinGw ]] ; then
  pip install virtualenv && pip install virtualenvwrapper-win
else
  sudo apt install virtualenv
fi
echo "Done!"

echo "Creating .venv and activate it..."
if [[ "$machine" == MinGw ]] ; then
  source .venv/bin/activate
else
  source source .venv/Scripts/activate
fi
echo "Done!"

# Check if script running in venv
python -c 'import sys; print(sys.real_prefix)' 2>/dev/null && INVENV=1 || INVENV=0

if [[ $INVENV == 1 ]] ; then
  pip3 install -r requirements.txt
else
  if [ "$machine" == MinGw ] ; then
    source .venv/Scripts/activate && pip3 install -r requirements.txt
  else
    source .venv/bin/activate && pip3 install -r requirements.txt
  fi
fi
echo "Done!"
