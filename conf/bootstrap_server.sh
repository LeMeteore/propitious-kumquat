#!/bin/sh

# not so well written shell script
# to make sure beloved packages are installed

apt-get update


# declare an array variable
# access: echo "${arr[0]}", "${arr[1]}"
declare -a pkgs=("redis-server" "emacs24-nox" "tmux" "git" "git-core" "python3" "python3-doc" "python3-dev" "python-setuptools" "uwsgi-plugin-python" "postgresql-contrib" "postgresql" "libpq-dev" "libjpeg-dev" "zlib1g-dev" "libpng12-dev" "gcc" "make" "build-essential" "fail2ban" "rkhunter" "chkrootkit")

## now loop through the above array
for i in "${pkgs[@]}"
do
  dpkg --get-selections | grep $i > /dev/null 2>&1
  if [ $? -ne 0 ]; then
      apt-get install --quiet --assume-yes $i
  fi
done

# install project requirements using pip
# if on on prod server, install requirements/prod.txt

# otherwise requirements/dev.txt
