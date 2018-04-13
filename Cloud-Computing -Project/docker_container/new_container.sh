#!/bin/bash
mkdir -p ~/.ssh
cd /home/fenics
mkdir  -p acc11
cd acc11
mkdir -p sync_results
cp /home/fenics/key /home/fenics/acc11
echo "host github.com
 HostName github.com
 IdentityFile /home/fenics/acc11/key
 User git" > ~/.ssh/config
chmod 700 ~/.ssh
cd /home/fenics/acc11
git clone git@github.com:Prekrim/Cloud-Computing-Airfoil.git
cd /home/fenics/acc11/Cloud-Computing-Airfoil
git checkout simon
git pull
cp id_rsa ~/.ssh/
cp id_rsa.pub ~/.ssh/
chmod 700 ~/.ssh
chmod 400 ~/.ssh/id_rsa
cp init_container.sh /home/fenics/acc11/
cp murtazo.tgz /home/fenics/acc11/
cd /home/fenics/acc11/
chmod +x init_container.sh
tar xzvf murtazo.tgz 
cd /home/fenics/acc11/murtazo/
tar xvf cloudnaca.tgz 
tar xvf navier_stokes_solver.tar 
cd /home/fenics/acc11/murtazo/navier_stokes_solver/src
./compile_forms 
cd /home/fenics/acc11/murtazo/navier_stokes_solver
cmake .
make -j 2
apt-get update
apt install python-pip
apt-get install gmsh
cd /home/fenics/acc11/murtazo/cloudnaca/
sed -i 's~^GMSHBIN.*$~GMSHBIN="/usr/bin/gmsh"~g' runme.sh
sed -i 's~^NACA1=.*$~NACA1="$6"~g' runme.sh
sed -i 's~^NACA2=.*$~NACA2="$7"~g' runme.sh
sed -i 's~^NACA3=.*$~NACA3="$8"~g' runme.sh
sed -i 's~^NACA4=.*$~NACA4="$9"~g' runme.sh
pip install celery
echo "container is now configured"

