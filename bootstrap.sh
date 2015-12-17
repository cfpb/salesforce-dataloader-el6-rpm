#!/usr/bin/env bash

sudo yum -y groupinstall 'Development Tools'

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

if [ "$SCRIPTPATH" = "/tmp" ] ; then
	SCRIPTPATH=/vagrant
fi

mkdir -p $HOME/rpmbuild/{BUILD,RPMS,SOURCES,SRPMS}
ln -s $SCRIPTPATH/SPECS $HOME/rpmbuild/SPECS
echo '%_topdir '$HOME'/rpmbuild' > $HOME/.rpmmacros

# Install java
sudo yum -y install java-1.8.0-openjdk-devel

# Install Maven
sudo mkdir -p /opt
sudo chmod 0777 /opt
cd /opt
wget http://apache.mirrors.pair.com/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
tar -xzvf apache-maven-3.3.9-bin.tar.gz
echo "export PATH=$PATH:/opt/apache-maven-3.3.9/bin" | sudo tee /etc/profile.d/maven.sh
echo "export JAVA_HOME=/usr/lib/jvm/java" | sudo tee /etc/profile.d/java.sh
chmod 644 /etc/profile.d/maven.sh
chmod 644 /etc/profile.d/java.sh

# Get Salesforce Dataloader source
git clone https://github.com/forcedotcom/dataloader
git submodule init
git submodule update
tar -cJvf sf-dataloader.tar.xz dataloader
cp sf-dataloader.tar.xz $HOME/rpmbuild/SOURCES/
