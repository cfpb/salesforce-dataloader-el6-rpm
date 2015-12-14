############################
# Set global SPEC variables
############################
%global prefix /usr
%global bindir %{prefix}/bin
%global libdir %{prefix}/lib

###############
# Set metadata
###############
Name: sf-dataloader
Version: 35.0.0
Release: 1
Summary: The Data Loader is an easy to use graphical tool that helps you to get your data into Salesforce objects.
Group: Applications/File
License: Salesforce
URL: https://github.com/forcedotcom/dataloader
Source: sf-dataloader.tar.xz
Obsoletes: sf-dataloader <= 35.0.0
Provides: sf-dataloader = 35.0.0

%description
The Data Loader is an easy to use graphical tool that helps you to get your data into Salesforce objects. The Data Loader can also be used to extract data from database objects into any of the destinations mentioned above. You can even use the Data Loader to perform bulk deletions by exporting the ID fields for the data you wish to delete and using that source to specify deletions through the Data Loader.

########################################################
# PREP and SETUP
# The prep directive removes existing build directory
# and extracts source code so we have a fresh
# code base.
########################################################
%prep
%setup -n dataloader

###########################################################
# BUILD
# The build directive does initial prep for building,
# then runs the configure script and then make to compile.
# Compiled code is placed in %{buildroot}
###########################################################
%build
mvn clean package -DskipTests

###########################################################
# INSTALL
# This directive is where the code is actually installed
# in the %{buildroot} folder in preparation for packaging.
###########################################################
%install
mkdir -p %{buildroot}%{bindir}/
mkdir -p %{buildroot}%{libdir}/sf-dataloader
mkdir -p %{buildroot}etc/sf-dataloader

# Example config file
cp src/test/resources/testfiles/conf/config.properites %{buildroot}etc/sf-dataloader/

# The Dataloader itself
cp target/dataloader-35.0-uber.jar %{buildroot}%{libdir}/sf-dataloader/

# A script to execute
echo "java -cp %{libdir}/sf-dataloader/dataloader-35.0-uber.jar -Dsalesforce.config.dir=/etc/sf-dataloader com.salesforce.dataloader.process.ProcessRunner" > %{buildroot}%{bindir}/sf-dataloader
chmod a+x %{buildroot}%{bindir}/sf-dataloader

###########################################################
# CLEAN
# This directive is for cleaning up post packaging, simply
# removes the buildroot directory in this case.
###########################################################
%clean
# Sanity check before removal of old buildroot files
[ -d "%{buildroot}" -a "%{buildroot}" != "/" ] && rm -rf %{buildroot}

##############################################################
# FILES
# The files directive must list all files that were installed
# so that they can be included in the package.
##############################################################
%files
%defattr(-,root,root,-)
%{bindir}/*
/etc/*
%{libdir}/*

# This directive is for changes made post release.
%changelog
