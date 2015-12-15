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
mvn clean package -U -e -DskipTests

###########################################################
# INSTALL
# This directive is where the code is actually installed
# in the %{buildroot} folder in preparation for packaging.
###########################################################
%install
mkdir -p %{buildroot}%{bindir}/
mkdir -p %{buildroot}%{libdir}/sf-dataloader
mkdir -p %{buildroot}/etc/sf-dataloader

# Example config file
cp src/test/resources/testfiles/conf/config.properties %{buildroot}/etc/sf-dataloader/
chmod a+r %{buildroot}/etc/sf-dataloader/config.properties

# The Dataloader itself
cp target/dataloader-35.0.0-uber.jar %{buildroot}%{libdir}/sf-dataloader/

# A script to execute the cli
echo "if [ ! -e \$HOME/.sf-dataloader/config.properties ]; then" > %{buildroot}%{bindir}/sf-dataloader
echo "  mkdir -p \$HOME/.sf-dataloader" >> %{buildroot}%{bindir}/sf-dataloader
echo "  cp /etc/sf-dataloader/config.properties \$HOME/.sf-dataloader/config.properties"  >> %{buildroot}%{bindir}/sf-dataloader
echo "  echo 'A config script has been added at ~/.sf-dataloader/config.properites'.  Please enter your Salesforce settings to use sf-dataloader." >> %{buildroot}%{bindir}/sf-dataloader
echo "  exit 0" >> %{buildroot}%{bindir}/sf-dataloader
echo "fi" >> %{buildroot}%{bindir}/sf-dataloader
echo "java -cp %{libdir}/sf-dataloader/dataloader-35.0.0-uber.jar -Dsalesforce.config.dir=\$HOME/.sf-dataloader com.salesforce.dataloader.process.ProcessRunner \"\$@\"" >> %{buildroot}%{bindir}/sf-dataloader

# A script to execute the gui
echo "java -jar %{libdir}/sf-dataloader/dataloader-35.0.0-uber.jar \"\$@\"" > %{buildroot}%{bindir}/sf-dataloader-gui

# A script file for generating an encrypted password
echo "java -cp %{libdir}/sf-dataloader/dataloader-35.0.0-uber.jar com.salesforce.dataloader.security.EncryptionUtil \"\$@\"" > %{buildroot}%{bindir}/sf-encrypt

chmod a+x %{buildroot}%{bindir}/sf-dataloader
chmod a+x %{buildroot}%{bindir}/sf-dataloader-gui
chmod a+x %{buildroot}%{bindir}/sf-encrypt

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
/etc/sf-dataloader/*
%{bindir}/*
%{libdir}/*

# This directive is for changes made post release.
%changelog
