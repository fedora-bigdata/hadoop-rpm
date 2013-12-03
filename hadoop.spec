%global _hardened_build 1

# Currently disabled because httpfs wants to download a copy of tomcat
# for the start scripts and config files.  The scripts aren't packaged
# so there's no means to substitute from rpms
%global package_httpfs 0

# libhdfs is only supported on intel architectures atm.
%ifarch %ix86 x86_64
%global package_libhdfs 1
%else
%global package_libhdfs 0
%endif

%global commit 2e01e27e5ba4ece19650484f646fac42596250ce
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global hadoop_version %{version}
%global hdfs_services hadoop-zkfc.service hadoop-datanode.service hadoop-secondarynamenode.service hadoop-namenode.service
%global mapreduce_services hadoop-historyserver.service
%global yarn_services hadoop-proxyserver.service hadoop-resourcemanager.service hadoop-nodemanager.service
%global httpfs_services hadoop-httpfs.service

# Filter out undesired provides and requires
%global __requires_exclude_from ^%{_libdir}/%{name}/libhadoop.so$
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$

Name:   hadoop
Version: 2.2.0
Release: 1%{?dist}
Summary: A software platform for processing vast amounts of data
# The BSD license file is missing
# https://issues.apache.org/jira/browse/HADOOP-9849
License: ASL 2.0 and BSD
Group:  Development/Libraries
URL: http://hadoop.apache.org
Source0: https://github.com/apache/hadoop-common/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1: hadoop-layout.sh
Source2: hadoop-hdfs.service.template
Source3: hadoop-mapreduce.service.template
Source4: hadoop-yarn.service.template
Source5: hadoop-httpfs.service
Source6: hadoop.logrotate
Source7: hadoop-limits.conf
Source8: hadoop-core-site.xml
Source9: hadoop-hdfs-site.xml
Source10: hadoop-mapred-site.xml
Source11: hadoop-yarn-site.xml
Source12: hadoop-httpfs-env.sh
Source13: hdfs-create-dirs
# This patch includes the following upstream tickets:
# https://issues.apache.org/jira/browse/HADOOP-9594
# https://issues.apache.org/jira/browse/MAPREDUCE-5431
# https://issues.apache.org/jira/browse/HADOOP-9611
# https://issues.apache.org/jira/browse/HADOOP-9613
# https://issues.apache.org/jira/browse/HADOOP-9623
# https://issues.apache.org/jira/browse/HDFS-5411
# https://issues.apache.org/jira/browse/HADOOP-10067
# https://issues.apache.org/jira/browse/HDFS-5075
# https://issues.apache.org/jira/browse/HADOOP-10068
# https://issues.apache.org/jira/browse/HADOOP-10075
# https://issues.apache.org/jira/browse/HADOOP-10076
Patch0: hadoop-fedora-integration.patch
# Fedora packaging guidelines for JNI library loading
Patch2: hadoop-jni-library-loading.patch
# Clean up warnings with maven 3.0.5
Patch3: hadoop-maven.patch
# Don't download tomcat.  This is incompatible with building httpfs
Patch4: hadoop-no-download-tomcat.patch
# Use dlopen to find libjvm.so
Patch5: hadoop-dlopen-libjvm.patch
# The native bits don't compile on ARM
ExcludeArch: %{arm}

# This is not a real BR, but is here because of rawhide shift to eclipse
# aether packages which caused a dependency of a dependency to not get
# pulled in.
BuildRequires: aether

BuildRequires: ant
BuildRequires: antlr-tool
BuildRequires: aopalliance
BuildRequires: apache-commons-beanutils
BuildRequires: apache-commons-cli
BuildRequires: apache-commons-collections
BuildRequires: apache-commons-configuration
BuildRequires: apache-commons-daemon
BuildRequires: apache-commons-el
BuildRequires: apache-commons-io
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-logging
BuildRequires: apache-commons-math
BuildRequires: apache-commons-net
BuildRequires: apache-rat-plugin
BuildRequires: atinject
BuildRequires: avalon-framework
BuildRequires: avalon-logkit
BuildRequires: avro
BuildRequires: bookkeeper-java
BuildRequires: cglib
BuildRequires: checkstyle
BuildRequires: chrpath
BuildRequires: cmake
BuildRequires: commons-codec
BuildRequires: commons-httpclient
%if %{package_httpfs}
BuildRequires: ecj >= 1:4.2.1-6
%endif
BuildRequires: fuse-devel
BuildRequires: fusesource-pom
BuildRequires: geronimo-jms
BuildRequires: gcc-c++
BuildRequires: glassfish-jaxb
BuildRequires: glassfish-jsp
BuildRequires: glassfish-jsp-api
BuildRequires: google-guice
BuildRequires: grizzly
BuildRequires: guava
BuildRequires: guice-servlet
BuildRequires: hamcrest
BuildRequires: hsqldb
BuildRequires: httpcomponents-client
BuildRequires: httpcomponents-core
BuildRequires: istack-commons
BuildRequires: jackson
BuildRequires: java-base64
BuildRequires: java-devel
BuildRequires: java-xmlbuilder
BuildRequires: javamail
BuildRequires: javapackages-tools
BuildRequires: jdiff
BuildRequires: jersey
BuildRequires: jersey-contribs
BuildRequires: jets3t
BuildRequires: jettison
# May need to break down into specific jetty rpms
BuildRequires: jetty
BuildRequires: jetty-jspc-maven-plugin
BuildRequires: jetty-util-ajax
BuildRequires: jsch
BuildRequires: json_simple
BuildRequires: jsr-305
BuildRequires: jsr-311
BuildRequires: junit
BuildRequires: jzlib
BuildRequires: log4j
BuildRequires: make
BuildRequires: maven
BuildRequires: maven-antrun-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-clean-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-dependency-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-invoker-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-local
BuildRequires: maven-plugin-build-helper
BuildRequires: maven-plugin-cobertura
BuildRequires: maven-plugin-exec
BuildRequires: maven-plugin-plugin
BuildRequires: maven-release-plugin
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-shade-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-war-plugin
BuildRequires: mockito
BuildRequires: native-maven-plugin
BuildRequires: netty
BuildRequires: objectweb-asm
BuildRequires: objenesis >= 1.2-16
BuildRequires: openssl-devel
BuildRequires: paranamer
BuildRequires: protobuf-compiler
BuildRequires: protobuf-java
BuildRequires: relaxngDatatype
BuildRequires: servlet3
BuildRequires: slf4j
BuildRequires: snappy-devel
BuildRequires: snappy-java
BuildRequires: systemd
BuildRequires: tomcat-el-2.2-api
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: txw2
BuildRequires: which
BuildRequires: xmlenc
BuildRequires: znerd-oss-parent
BuildRequires: zookeeper-java

# For tests
BuildRequires: jersey-test-framework
BuildRequires: maven-surefire-provider-junit4

%description
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

%package client
Summary: Libraries for Apache Hadoop clients
Group: Applications/System
BuildArch: noarch
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}

%description client
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides libraries for Apache Hadoop clients.

%package common
Summary: Common files needed by Apache Hadoop daemons
Group: Applications/System
BuildArch: noarch
Requires: /usr/sbin/useradd

# These are required to meet the symlinks for the classpath
Requires: antlr-tool
Requires: apache-commons-beanutils
Requires: avalon-framework
Requires: avalon-logkit
Requires: checkstyle
Requires: commons-httpclient
Requires: coreutils
Requires: geronimo-jms
Requires: glassfish-jaxb
Requires: glassfish-jsp
Requires: glassfish-jsp-api
Requires: istack-commons
Requires: java
Requires: java-base64
Requires: java-xmlbuilder
Requires: javamail
Requires: jettison
Requires: jetty-http
Requires: jetty-io
Requires: jetty-security
Requires: jetty-xml
Requires: jline
Requires: jsr-311
Requires: mockito
Requires: nc6
Requires: objectweb-asm
Requires: objenesis
Requires: paranamer
Requires: relaxngDatatype
Requires: servlet3
Requires: snappy-java
Requires: txw2
Requires: which

%description common
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains common files and utilities needed by other Apache
Hadoop modules.

%package common-native
Summary: The native Apache Hadoop library file
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}

%description common-native
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains the native-hadoop library

%if %{package_libhdfs}
%package devel
Summary: Headers for Apache Hadoop
Group: Development/System
Requires: libhdfs%{?_isa} = %{version}-%{release}

%description devel
Header files for Apache Hadoop's hdfs library and other utilities
%endif

%package hdfs
Summary: The Apache Hadoop Distributed File System
Group: Applications/System
BuildArch: noarch
Requires: apache-commons-daemon-jsvc
Requires: %{name}-common = %{version}-%{release}
Requires(pre): %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description hdfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

The Hadoop Distributed File System (HDFS) is the primary storage system
used by Apache Hadoop applications.

%if %{package_libhdfs}
%package hdfs-fuse
Summary: Allows mounting of Apache Hadoop HDFS
Group: Development/Libraries
Requires: fuse
Requires: libhdfs%{?_isa} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}

%description hdfs-fuse
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides tools that allow HDFS to be mounted as a standard
file system through fuse.
%endif

%if %{package_httpfs}
%package httpfs
Summary: Provides web access to HDFS
Group: Applications/System
BuildArch: noarch
Requires: apache-commons-dbcp
Requires: ecj >= 1:4.2.1-6
Requires: tomcat
Requires: tomcat-lib
Requires: tomcat-native
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description httpfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides a server that provides HTTP REST API support for
the complete FileSystem/FileContext interface in HDFS.
%endif

# Creation of javadocs takes too many resources and results in failures  on
# most architectures so only generate on intel 64-bit
%ifarch x86_64
%package javadoc
Summary: Javadoc for Apache Hadoop
Group: Documentation
BuildArch: noarch

%description javadoc
This package contains the API documentation for %{name}.
%endif

%if %{package_libhdfs}
%package -n libhdfs
Summary: The Apache Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
Requires: lzo

%description -n libhdfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides the Apache Hadoop Filesystem Library.
%endif

%package mapreduce
Summary: Apache Hadoop MapReduce (MRv2)
Group: Applications/System
BuildArch: noarch
Requires(pre): %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description mapreduce
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides Apache Hadoop MapReduce (MRv2).

%package mapreduce-examples
Summary: Apache Hadoop MapReduce (MRv2) examples
Group: Applications/System
BuildArch: noarch
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: hsqldb

%description mapreduce-examples
This package contains mapreduce examples.

%package maven-plugin
Summary: Apache Hadoop maven plugin
Group: Development/Libraries
BuildArch: noarch
Requires: maven

%description maven-plugin
The Apache Hadoop maven plugin

%package tests
Summary: Apache Hadoop test resources
BuildArch: noarch
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}

%description tests
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains test related resources for Apache Hadoop.

%package yarn
Summary: Apache Hadoop YARN
Group: Applications/System
BuildArch: noarch
Requires(pre): %{name}-common = %{version}-%{release}
Requires: aopalliance
Requires: atinject
Requires: hamcrest
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description yarn
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains Apache Hadoop YARN.

%package yarn-security
Summary: The ability to run Apache Hadoop YARN in secure mode
Group: Applications/System
Requires: %{name}-yarn = %{version}-%{release}

%description yarn-security
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains files needed to run Apache Hadoop YARN in secure mode.

%prep
%setup -qn %{name}-common-%{commit}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%if 0%{package_httpfs} == 0
%patch4 -p1
%endif
%if %{package_libhdfs}
%patch5 -p1
%endif

# The hadoop test suite needs classes from the zookeeper test suite.
# We need to modify the deps to use the pom for the zookeeper-test jar
%pom_remove_dep org.apache.zookeeper:zookeeper hadoop-common-project/hadoop-common
%pom_add_dep org.apache.zookeeper:zookeeper hadoop-common-project/hadoop-common
%pom_add_dep org.apache.zookeeper:zookeeper-test hadoop-common-project/hadoop-common
%pom_remove_dep org.apache.zookeeper:zookeeper hadoop-hdfs-project/hadoop-hdfs
%pom_add_dep org.apache.zookeeper:zookeeper-test hadoop-hdfs-project/hadoop-hdfs
%pom_remove_dep org.apache.zookeeper:zookeeper hadoop-hdfs-project/hadoop-hdfs-nfs
%pom_add_dep org.apache.zookeeper:zookeeper-test hadoop-hdfs-project/hadoop-hdfs-nfs

# Remove the maven-site-plugin.  It's not needed
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-site-plugin hadoop-common-project/hadoop-auth
%pom_remove_plugin :maven-site-plugin hadoop-hdfs-project/hadoop-hdfs-httpfs

# Remove the findbugs-maven-plugin.  It's not needed and isn't available
%pom_remove_plugin :findbugs-maven-plugin hadoop-hdfs-project/hadoop-hdfs-httpfs
%pom_remove_plugin :findbugs-maven-plugin hadoop-hdfs-project/hadoop-hdfs/src/contrib/bkjournal
%pom_remove_plugin :findbugs-maven-plugin hadoop-mapreduce-project/hadoop-mapreduce-client
%pom_remove_plugin :findbugs-maven-plugin hadoop-mapreduce-project/hadoop-mapreduce-examples
%pom_remove_plugin :findbugs-maven-plugin hadoop-mapreduce-project
%pom_remove_plugin :findbugs-maven-plugin hadoop-project-dist
%pom_remove_plugin :findbugs-maven-plugin hadoop-project
%pom_remove_plugin :findbugs-maven-plugin hadoop-tools/hadoop-rumen
%pom_remove_plugin :findbugs-maven-plugin hadoop-tools/hadoop-streaming
%pom_remove_plugin :findbugs-maven-plugin hadoop-yarn-project/hadoop-yarn
%pom_remove_plugin :findbugs-maven-plugin hadoop-yarn-project

# Remove the maven-project-info-reports plugin.  It's not needed and isn't available
%pom_remove_plugin :maven-project-info-reports-plugin hadoop-common-project/hadoop-auth
%pom_remove_plugin :maven-project-info-reports-plugin hadoop-hdfs-project/hadoop-hdfs-httpfs
%pom_remove_plugin :maven-project-info-reports-plugin hadoop-project

# Remove the maven-checkstyle plugin.  It's not needed and isn't available
%pom_remove_plugin :maven-checkstyle-plugin hadoop-project-dist
%pom_remove_plugin :maven-checkstyle-plugin hadoop-project
%pom_remove_plugin :maven-checkstyle-plugin hadoop-tools/hadoop-distcp

# War files we don't want
%mvn_package :%{name}-auth-examples __noinstall
%mvn_package :%{name}-hdfs-httpfs __noinstall

# Parts we don't want to distribute
%mvn_package :%{name}-assemblies __noinstall

# Workaround for bz1012059
%mvn_package :%{name}-project-dist __noinstall

# Create separate file lists for packaging
%mvn_package :::tests: %{name}-tests
%mvn_package :%{name}-client*::{}: %{name}-client
%mvn_package :%{name}-hdfs*::{}: %{name}-hdfs
%mvn_package :%{name}-mapreduce-examples*::{}: %{name}-mapreduce-examples
%mvn_package :%{name}-mapreduce*::{}: %{name}-mapreduce
%mvn_package :%{name}-archives::{}: %{name}-mapreduce
%mvn_package :%{name}-datajoin::{}: %{name}-mapreduce
%mvn_package :%{name}-distcp::{}: %{name}-mapreduce
%mvn_package :%{name}-extras::{}: %{name}-mapreduce
%mvn_package :%{name}-gridmix::{}: %{name}-mapreduce
%mvn_package :%{name}-rumen::{}: %{name}-mapreduce
%mvn_package :%{name}-streaming::{}: %{name}-mapreduce
%mvn_package :%{name}-pipes::{}: %{name}-mapreduce
%mvn_package :%{name}-tools*::{}: %{name}-mapreduce
%mvn_package :%{name}-maven-plugins::{}: %{name}-maven-plugin
%mvn_package :%{name}-minicluster::{}: %{name}-tests
%mvn_package :%{name}-yarn*::{}: %{name}-yarn

# Jar files that need to be overridden due to installation location
# Workaround for bz1023116
#%%mvn_file :%{name}-common::{}: %{_jnidir}/%{name}-common %{_datadir}/%{name}/common/%{name}-common
%mvn_file :%{name}-common::{}: %{_jnidir}/%{name}-common
%mvn_file :%{name}-common::tests: %{name}/%{name}-common

%build
%ifnarch x86_64
opts="-j"
%endif
%mvn_build $opts -- -Drequire.snappy=true -Dcontainer-executor.conf.dir=%{_sysconfdir}/%{name} -Pdist,native -DskipTests -DskipTest -DskipIT

# This takes a long time to run, so comment out for now
#%%check
#mvn-rpmbuild -Pdist,native test -Dmaven.test.failure.ignore=true

%install
# Creates symlinks for dependency jars into a specificed directory and will
# append the files to the filelist
# $1 the directory to create the smlinks
# $2 the filelist to append to
# $* the list of jars to link
link_jars()
{
  dir=$1
  list=$2
  shift 2
  files=$*

  for pattern in $files
  do 
    for file in `%{_bindir}/build-classpath $pattern | tr ":" "\\n"` 
    do 
      %{__ln_s} $file %{buildroot}/$dir
      if [[ ! -z "$list" ]]
      then
        echo "$dir/$(basename $file)" >> $list
      fi
    done 
  done 
}

# Copy all jar files except those generated by the build
# $1 the src directory
# $2 the dest directory
copy_dep_jars()
{
  find $1 ! -name "hadoop-*.jar" -name "*.jar" | xargs install -m 0644 -t $2
  rm -f $2/tools-*.jar
}

# Create a pom file for a test jar
# $1 what the test jar is associated with
create_test_pom()
{
  dep=`echo $1 | sed "s/-tests//g"`
  pom="JPP.%{name}-$1.pom"
  cat > %{buildroot}%{_mavenpomdir}/$pom << EOL
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.apache.hadoop</groupId>
  <artifactId>$1</artifactId>
  <version>%{hadoop_version}</version>

  <dependencies>
    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>$dep</artifactId>
      <version>%{hadoop_version}</version>
    </dependency>
  </dependencies>
</project>
EOL
  %add_maven_depmap -f %{name}-tests $pom %{name}/$1.jar
}

%mvn_install

install -d -m 0755 %{buildroot}/%{_libdir}/%{name}
install -d -m 0755 %{buildroot}/%{_includedir}/%{name}
install -d -m 0755 %{buildroot}/%{_jnidir}/

install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/client/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/common/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/hdfs/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/yarn/lib
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{name}-hdfs/webapps/hdfs
install -d -m 0755 %{buildroot}/%{_sysconfdir}/logrotate.d
install -d -m 0755 %{buildroot}/%{_tmpfilesdir}
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-hdfs
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-mapreduce
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-hdfs
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-mapreduce
install -d -m 0755 %{buildroot}/%{_var}/run/%{name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/run/%{name}-hdfs
install -d -m 0755 %{buildroot}/%{_var}/run/%{name}-mapreduce
%if %{package_httpfs}
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/bin
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/lib
install -d -m 0755 %{buildroot}/%{_libexecdir}/%{name}-httpfs
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{name}-httpfs/webapps
install -d -m 0755 %{buildroot}/%{_sysconfdir}/%{name}/httpfs-tomcat/Catalina/localhost
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-httpfs/work
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-httpfs/temp
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-httpfs
install -d -m 0755 %{buildroot}/%{_var}/run/%{name}-httpfs
%endif

basedir='%{name}-dist/target/%{name}-%{hadoop_version}'

for dir in bin libexec sbin
do
  cp -arf $basedir/$dir %{buildroot}/%{_prefix}
done

# This binary is obsoleted and causes a conflict with qt-devel
rm -rf %{buildroot}/%{_bindir}/rcc

# We don't care about this
rm -f %{buildroot}/%{_bindir}/test-container-executor

# Duplicate files
rm -f %{buildroot}/%{_sbindir}/hdfs-config.sh

cp -arf $basedir/etc/* %{buildroot}/%{_sysconfdir}
cp -arf $basedir/lib/native/libhadoop.so* %{buildroot}/%{_libdir}/%{name}
chrpath --delete %{buildroot}/%{_libdir}/%{name}/*
%if %{package_libhdfs}
cp -arf $basedir/include/hdfs.h %{buildroot}/%{_includedir}/%{name}
cp -arf $basedir/lib/native/libhdfs.so* %{buildroot}/%{_libdir}
chrpath --delete %{buildroot}/%{_libdir}/libhdfs*
cp -af hadoop-hdfs-project/hadoop-hdfs/target/native/main/native/fuse-dfs/fuse_dfs %{buildroot}/%{_bindir}
chrpath --delete %{buildroot}/%{_bindir}/fuse_dfs
%endif

%if 0%{package_httpfs} == 0
rm -f %{buildroot}/%{_sbindir}/httpfs.sh
rm -f %{buildroot}/%{_libexecdir}/httpfs-config.sh
rm -f %{buildroot}/%{_sysconfdir}/%{name}/httpfs*
%endif

# Remove files with .cmd extension
find %{buildroot} -name *.cmd | xargs rm -f 

# Modify hadoop-env.sh to point to correct locations for JAVA_HOME
# and JSVC_HOME.
sed -i "s|\${JAVA_HOME}|/usr/lib/jvm/jre|" %{buildroot}/%{_sysconfdir}/%{name}/%{name}-env.sh
sed -i "s|\${JSVC_HOME}|/usr/bin|" %{buildroot}/%{_sysconfdir}/%{name}/%{name}-env.sh

# Ensure the java provided DocumentBuilderFactory is used
sed -i "s|\(HADOOP_OPTS.*=.*\)\$HADOOP_CLIENT_OPTS|\1 -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl \$HADOOP_CLIENT_OPTS|" %{buildroot}/%{_sysconfdir}/%{name}/%{name}-env.sh
echo "export YARN_OPTS=\"\$YARN_OPTS -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl\"" >> %{buildroot}/%{_sysconfdir}/%{name}/yarn-env.sh

# Workaround for bz1012059
install -pm 644 %{name}-project-dist/target/%{name}-project-dist-%{hadoop_version}.jar %{buildroot}/%{_javadir}/%{name}/%{name}-project-dist.jar
install -pm 644 hadoop-project-dist/pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}-%{name}-project-dist.pom
%add_maven_depmap JPP.%{name}-%{name}-project-dist.pom %{name}/%{name}-project-dist.jar

# Workaround for bz1023116
%{__ln_s} %{_jnidir}/%{name}-common.jar %{buildroot}/%{_datadir}/%{name}/common

# client jar depenencies
copy_dep_jars %{name}-client/target/%{name}-client-%{hadoop_version}/share/%{name}/client/lib %{buildroot}/%{_datadir}/%{name}/client/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/client/lib
%{__ln_s} %{_jnidir}/%{name}-common.jar %{buildroot}/%{_datadir}/%{name}/client/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-client.jar %{buildroot}/%{_datadir}/%{name}/client
for f in annotations auth hdfs mapreduce-client-app mapreduce-client-common mapreduce-client-core mapreduce-client-jobclient mapreduce-client-shuffle yarn-api yarn-client yarn-common yarn-server-common
do
  %{__ln_s} %{_javadir}/%{name}/%{name}-$f.jar %{buildroot}/%{_datadir}/%{name}/client/lib
done

# common jar depenencies
copy_dep_jars $basedir/share/%{name}/common/lib %{buildroot}/%{_datadir}/%{name}/common/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/common/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-nfs.jar %{buildroot}/%{_datadir}/%{name}/common
echo "%{_datadir}/%{name}/common/%{name}-nfs.jar" >> .mfiles
for f in annotations auth
do
  %{__ln_s} %{_javadir}/%{name}/%{name}-$f.jar %{buildroot}/%{_datadir}/%{name}/common/lib
done

# hdfs jar dependencies
copy_dep_jars $basedir/share/%{name}/hdfs/lib %{buildroot}/%{_datadir}/%{name}/hdfs/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/hdfs/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-hdfs.jar %{buildroot}/%{_datadir}/%{name}/hdfs
%{__ln_s} %{_javadir}/%{name}/%{name}-hdfs-nfs.jar %{buildroot}/%{_datadir}/%{name}/hdfs
%{__ln_s} %{_javadir}/%{name}/%{name}-hdfs-bkjournal.jar %{buildroot}/%{_datadir}/%{name}/hdfs/lib

# httpfs
%if %{package_httpfs}
# Remove and replace with symlinks once tomcat scripts are packaged
cp -arf $basedir/share/hadoop/httpfs/tomcat/bin/*.sh %{buildroot}/%{_libexecdir}/%{name}-httpfs
cp -arf $basedir/share/hadoop/httpfs/tomcat/bin/catalina-tasks.xml %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/bin

install -m 644 $basedir/share/hadoop/httpfs/tomcat/conf/* %{buildroot}/%{_sysconfdir}/%{name}/httpfs-tomcat
cp -arf $basedir/share/hadoop/httpfs/tomcat/webapps %{buildroot}/%{_sharedstatedir}/%{name}-httpfs

# Tell tomcat to follow symlinks
cat > %{buildroot}/%{_sharedstatedir}/%{name}-httpfs/webapps/webhdfs/META-INF/context.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<Context allowLinking="true">
</Context>
EOF

# Remove the jars included in the webapp and create symlinks
rm -f %{buildroot}%{_sharedstatedir}/%{name}-httpfs/webapps/webhdfs/WEB-INF/lib/%{name}-common*.jar
rm -f %{buildroot}%{_sharedstatedir}/%{name}-httpfs/webapps/webhdfs/WEB-INF/lib/tools*.jar
%{_bindir}/xmvn-subst %{buildroot}/%{_sharedstatedir}/%{name}-httpfs/webapps/webhdfs/WEB-INF/lib
%{__ln_s} %{_jnidir}/%{name}-common.jar %{buildroot}%{_sharedstatedir}/%{name}-httpfs/webapps/webhdfs/WEB-INF/lib
#link_jars %{_sharedstatedir}/%{name}-httpfs/webapps/webhdfs/WEB-INF/lib nil antlr objectweb-asm/asm avalon-framework-api avalon-logkit avro/avro cglib checkstyle commons-beanutils-core commons-cli commons-codec commons-collections commons-configuration commons-daemon commons-io commons-lang commons-logging commons-math3 commons-net guava hamcrest/core istack-commons-runtime jackson/jackson-core-asl jackson/jackson-jaxrs jackson/jackson-mapper-asl jackson/jackson-xc glassfish-jsp glassfish-jsp-api glassfish-jaxb/jaxb-impl jersey/jersey-core jersey/jersey-json jersey/jersey-server jersey/jersey-servlet jettison jetty/jetty-util jetty/jetty-util-ajax jline jms jsch json_simple jsr-305 jsr-311 jzlib log4j javamail/mail mockito netty objenesis paranamer/paranamer protobuf slf4j/api slf4j/log4j12 snappy-java txw2 xmlenc zookeeper/zookeeper

# xmvn-subst won't work with d/led jars
#copy_dep_jars $basedir/share/hadoop/httpfs/tomcat/bin %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/bin
#%%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/bin
link_jars %{_datadir}/%{name}/httpfs/tomcat/bin nil tomcat/tomcat-juli commons-daemon

# xmvn-subst won't work with d/led jars
#copy_dep_jars $basedir/share/hadoop/httpfs/tomcat/lib %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/lib
#%%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/lib
link_jars %{_datadir}/%{name}/httpfs/tomcat/lib nil tomcat/annotations-api tomcat/catalina-ant tomcat/catalina-ha tomcat/catalina tomcat/catalina-tribes ecj tomcat/tomcat-el-2.2-api tomcat/jasper-el tomcat/jasper glassfish-jsp-api tomcat/tomcat-api tomcat/tomcat-jsp-2.2-api tomcat-servlet-api tomcat/tomcat-coyote tomcat/tomcat-util commons-dbcp tomcat/tomcat-i18n-es tomcat/tomcat-i18n-fr tomcat/tomcat-i18n-ja

pushd %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat
  %{__ln_s} %{_datadir}/tomcat/bin/bootstrap.jar bin
  for f in `ls %{buildroot}/%{_libexecdir}/%{name}-httpfs`
  do
    %{__ln_s} %{_libexecdir}/%{name}-httpfs/$f bin
  done
  %{__ln_s} %{_sysconfdir}/%{name}/httpfs-tomcat conf 
  %{__ln_s} %{_var}/log/%{name}-httpfs logs
  %{__ln_s} %{_sharedstatedir}/%{name}-httpfs/webapps webapps
  %{__ln_s} %{_var}/cache/%{name}-httpfs/temp temp
  %{__ln_s} %{_var}/cache/%{name}-httpfs/work work
popd
%endif

# mapreduce jar dependencies
copy_dep_jars $basedir/share/%{name}/mapreduce/lib %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-annotations.jar %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
for f in app common core jobclient shuffle hs hs-plugins
do
  %{__ln_s} %{_javadir}/%{name}/%{name}-mapreduce-client-$f.jar %{buildroot}/%{_datadir}/%{name}/mapreduce
done
for f in archives datajoin distcp extras gridmix rumen streaming
do
  %{__ln_s} %{_javadir}/%{name}/%{name}-$f.jar %{buildroot}/%{_datadir}/%{name}/mapreduce
done

# yarn jar dependencies
copy_dep_jars $basedir/share/%{name}/yarn/lib %{buildroot}/%{_datadir}/%{name}/yarn/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/yarn/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-annotations.jar %{buildroot}/%{_datadir}/%{name}/yarn/lib
for f in api client common server-common applications-distributedshell applications-unmanaged-am-launcher server-nodemanager server-resourcemanager server-web-proxy site
do
  %{__ln_s} %{_javadir}/%{name}/%{name}-yarn-$f.jar %{buildroot}/%{_datadir}/%{name}/yarn
done

# Install hdfs webapp bits
cp -arf $basedir/share/hadoop/hdfs/webapps/* %{buildroot}/%{_sharedstatedir}/%{name}-hdfs/webapps
pushd %{buildroot}/%{_datadir}/%{name}/hdfs
  %{__ln_s} %{_sharedstatedir}/%{name}-hdfs/webapps webapps
popd

# hadoop layout. Convert to appropriate lib location for 32 and 64 bit archs
lib=$(echo %{?_libdir} | sed -e 's:/usr/\(.*\):\1:')
if [ "$lib" = "%_libdir" ]; then
  echo "_libdir is not located in /usr.  Lib location is wrong"
  exit 1
fi
sed -e "s|HADOOP_COMMON_LIB_NATIVE_DIR\s*=.*|HADOOP_COMMON_LIB_NATIVE_DIR=$lib/%{name}|" %{SOURCE1} > %{buildroot}/%{_libexecdir}/%{name}-layout.sh

# Default config
cp -f %{SOURCE8} %{buildroot}/%{_sysconfdir}/%{name}/core-site.xml
cp -f %{SOURCE9} %{buildroot}/%{_sysconfdir}/%{name}/hdfs-site.xml
cp -f %{SOURCE10} %{buildroot}/%{_sysconfdir}/%{name}/mapred-site.xml
cp -f %{SOURCE11} %{buildroot}/%{_sysconfdir}/%{name}/yarn-site.xml

# systemd configuration
install -d -m 0755 %{buildroot}/%{_unitdir}/
for service in %{hdfs_services} %{mapreduce_services} %{yarn_services}
do
  s=`echo $service | cut -d'-' -f 2 | cut -d'.' -f 1`
  if [[ "%{hdfs_services}" == *$service* ]]
  then
    src=%{SOURCE2}
  elif [[ "%{mapreduce_services}" == *$service* ]]
  then
    src=%{SOURCE3}
  elif [[ "%{yarn_services}" == *$service* ]]
  then
    src=%{SOURCE4}
  else
    echo "Failed to determine type of service for %service"
    exit 1
  fi
  sed -e "s|DAEMON|$s|g" $src > %{buildroot}/%{_unitdir}/%{name}-$s.service
done

%if %{package_httpfs}
cp -f %{SOURCE5} %{buildroot}/%{_unitdir}
cp -f %{SOURCE12} %{buildroot}/%{_sysconfdir}/%{name}/httpfs-env.sh
%{__ln_s} %{_sysconfdir}/%{name}/httpfs-env.sh %{buildroot}/%{_bindir}
%endif

# Install security limits
install -d -m 0755 %{buildroot}/%{_sysconfdir}/security/limits.d
for limit in hdfs yarn mapreduce
do
  sed -e "s|name|${limit:0:6}|" %{SOURCE7} > %{buildroot}/%{_sysconfdir}/security/limits.d/${limit}.conf
done

# Ensure /var/run directories are recreated on boot
echo "d %{_var}/run/%{name}-yarn 0775 yarn hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{name}-yarn.conf
echo "d %{_var}/run/%{name}-hdfs 0775 hdfs hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{name}-hdfs.conf
echo "d %{_var}/run/%{name}-mapreduce 0775 mapred hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{name}-mapreduce.conf
%if %{package_httpfs}
echo "d %{_var}/run/%{name}-httpfs 0775 httpfs hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{name}-httpfs.conf
%endif

# logrotate config
sys_types="hdfs yarn mapreduce"
%if %{package_httpfs}
sys_types="$sys_types httpfs"
%endif

for type in $sys_types
do
  sed -e "s|NAME|$type|" %{SOURCE6} > %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}-$type
done
sed -i "s|{|%{_var}/log/hadoop-hdfs/*.audit\n{|" %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}-hdfs

# hdfs init script
install -m 755 %{SOURCE13} %{buildroot}/%{_sbindir}

# pom files for test jars
for f in `ls %{buildroot}/%{_javadir}/%{name}/%{name}-*-tests.jar %{buildroot}/%{_jnidir}/%{name}-*-tests.jar | grep -v yarn-server-tests`
do
  create_test_pom $(basename $f | sed "s/.jar//g")
done

install -m 0644 hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-tests/pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}-%{name}-yarn-server-tests-tests.pom
%add_maven_depmap -f %{name}-tests JPP.%{name}-%{name}-yarn-server-tests-tests.pom %{name}/%{name}-yarn-server-tests-tests.jar

%pre common
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop HDFS" --shell /sbin/nologin -M -r -g hdfs -G hadoop --home %{_var}/cache/%{name}-hdfs hdfs

%if %{package_httpfs}
%pre httpfs 
getent group httpfs >/dev/null || groupadd -r httpfs
getent passwd httpfs >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop HTTPFS" --shell /sbin/nologin -M -r -g httpfs -G httpfs --home %{_var}/run/%{name}-httpfs httpfs
%endif

%pre mapreduce
getent group mapred >/dev/null || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop MapReduce" --shell /sbin/nologin -M -r -g mapred -G hadoop --home %{_var}/cache/%{name}-mapreduce mapred

%pre yarn
getent group yarn >/dev/null || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop Yarn" --shell /sbin/nologin -M -r -g yarn -G hadoop --home %{_var}/cache/%{name}-yarn yarn

%preun hdfs
%systemd_preun %{hdfs_services}

%if %{package_httpfs}
%preun httpfs
%systemd_preun %{httpfs_services}
%endif

%preun mapreduce
%systemd_preun %{mapreduce_services}

%preun yarn
%systemd_preun %{yarn_services}

%post common-native -p /sbin/ldconfig

%post hdfs
%systemd_post %{hdfs_services}

%if %{package_httpfs}
%post httpfs
%systemd_post %{httpfs_services}
%endif

%if %{package_libhdfs}
%post -n libhdfs -p /sbin/ldconfig
%endif

%post mapreduce
%systemd_post %{mapreduce_services}

%post yarn
%systemd_post %{yarn_services}

%postun common-native -p /sbin/ldconfig

%postun hdfs
%systemd_postun_with_restart %{hdfs_services}

%if %{package_httpfs}
%postun httpfs
%systemd_postun_with_restart %{httpfs_services}
%endif

%if %{package_libhdfs}
%postun -n libhdfs -p /sbin/ldconfig
%endif

%postun mapreduce
%systemd_postun_with_restart %{mapreduce_services}

%postun yarn
%systemd_postun_with_restart %{yarn_services}

%files -f .mfiles-%{name}-client client
%{_datadir}/%{name}/client

%files -f .mfiles common
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/*
%config(noreplace) %{_sysconfdir}/%{name}/configuration.xsl
%config(noreplace) %{_sysconfdir}/%{name}/core-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-metrics.properties
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-metrics2.properties
%config(noreplace) %{_sysconfdir}/%{name}/%{name}-policy.xml
%config(noreplace) %{_sysconfdir}/%{name}/log4j.properties
%config(noreplace) %{_sysconfdir}/%{name}/slaves
%config(noreplace) %{_sysconfdir}/%{name}/ssl-client.xml.example
%config(noreplace) %{_sysconfdir}/%{name}/ssl-server.xml.example
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/common

# Workaround for bz1023116
%{_datadir}/%{name}/common/%{name}-common.jar

%{_datadir}/%{name}/common/lib
%{_libexecdir}/%{name}-config.sh
%{_libexecdir}/%{name}-layout.sh
%{_bindir}/%{name}
%{_sbindir}/%{name}-daemon.sh
%{_sbindir}/%{name}-daemons.sh
%{_sbindir}/start-all.sh
%{_sbindir}/start-balancer.sh
%{_sbindir}/start-dfs.sh
%{_sbindir}/start-secure-dns.sh
%{_sbindir}/stop-all.sh
%{_sbindir}/stop-balancer.sh
%{_sbindir}/stop-dfs.sh
%{_sbindir}/stop-secure-dns.sh
%{_sbindir}/slaves.sh

%files common-native
%{_libdir}/%{name}/libhadoop.*

%if %{package_libhdfs}
%files devel
%{_includedir}/%{name}
%{_libdir}/libhdfs.so
%endif

%files -f .mfiles-%{name}-hdfs hdfs
%exclude %{_datadir}/%{name}/client
%config(noreplace) %{_sysconfdir}/%{name}/hdfs-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/hdfs.conf
%{_datadir}/%{name}/hdfs
%attr(-,hdfs,hadoop) %{_sharedstatedir}/%{name}-hdfs
%{_unitdir}/%{name}-datanode.service
%{_unitdir}/%{name}-namenode.service
%{_unitdir}/%{name}-secondarynamenode.service
%{_unitdir}/%{name}-zkfc.service
%{_libexecdir}/hdfs-config.sh
%{_bindir}/hdfs
%{_sbindir}/distribute-exclude.sh
%{_sbindir}/refresh-namenodes.sh
%{_sbindir}/hdfs-create-dirs
%{_tmpfilesdir}/%{name}-hdfs.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/run/%{name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/log/%{name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/cache/%{name}-hdfs

%if %{package_libhdfs}
%files hdfs-fuse
%attr(755,hdfs,hadoop) %{_bindir}/fuse_dfs
%endif

%if %{package_httpfs}
%files httpfs
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-log4j.properties
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-signature.secret
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-tomcat/catalina.policy
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-tomcat/catalina.properties
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-tomcat/context.xml
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-tomcat/logging.properties
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-tomcat/server.xml
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-tomcat/tomcat-users.xml
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-tomcat/web.xml
%attr(0755,root,httpfs) %{_sysconfdir}/%{name}/httpfs-tomcat/Catalina
%{_bindir}/httpfs-env.sh
%{_libexecdir}/httpfs-config.sh
%{_libexecdir}/%{name}-httpfs
%{_unitdir}/%{name}-httpfs.service
%{_sbindir}/httpfs.sh
%{_datadir}/%{name}/httpfs
%attr(-,httpfs,httpfs) %{_sharedstatedir}/%{name}-httpfs
%{_tmpfilesdir}/%{name}-httpfs.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-httpfs
%attr(0755,httpfs,httpfs) %dir %{_var}/run/%{name}-httpfs
%attr(0755,httpfs,httpfs) %dir %{_var}/log/%{name}-httpfs
%attr(0755,httpfs,httpfs) %{_var}/cache/%{name}-httpfs
%endif

%ifarch x86_64
%files -f .mfiles-javadoc javadoc
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/LICENSE.txt hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/NOTICE.txt
%endif

%if %{package_libhdfs}
%files -n libhdfs
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/hdfs/LICENSE.txt
%{_libdir}/libhdfs.so.*
%endif

%files -f .mfiles-%{name}-mapreduce mapreduce
%exclude %{_datadir}/%{name}/client
%config(noreplace) %{_sysconfdir}/%{name}/mapred-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/mapred-queues.xml.template
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml.template
%config(noreplace) %{_sysconfdir}/security/limits.d/mapreduce.conf
%{_datadir}/%{name}/mapreduce
%{_libexecdir}/mapred-config.sh
%{_unitdir}/%{name}-historyserver.service
%{_bindir}/mapred
%{_sbindir}/mr-jobhistory-daemon.sh
%{_tmpfilesdir}/%{name}-mapreduce.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/run/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/log/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/cache/%{name}-mapreduce

%files -f .mfiles-%{name}-mapreduce-examples mapreduce-examples

%files -f .mfiles-%{name}-maven-plugin maven-plugin
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/LICENSE.txt

%files -f .mfiles-%{name}-tests tests

%files -f .mfiles-%{name}-yarn yarn
%exclude %{_datadir}/%{name}/client
%config(noreplace) %{_sysconfdir}/%{name}/capacity-scheduler.xml
%config(noreplace) %{_sysconfdir}/%{name}/yarn-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/yarn-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/yarn.conf
%{_unitdir}/%{name}-nodemanager.service
%{_unitdir}/%{name}-proxyserver.service
%{_unitdir}/%{name}-resourcemanager.service
%{_libexecdir}/yarn-config.sh
%{_datadir}/%{name}/yarn
%{_bindir}/yarn
%{_sbindir}/yarn-daemon.sh
%{_sbindir}/yarn-daemons.sh
%{_sbindir}/start-yarn.sh
%{_sbindir}/stop-yarn.sh
%{_tmpfilesdir}/%{name}-yarn.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/run/%{name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/log/%{name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/cache/%{name}-yarn

%files yarn-security
%config(noreplace) %{_sysconfdir}/%{name}/container-executor.cfg
# Permissions set per upstream guidelines: http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/ClusterSetup.html#Configuration_in_Secure_Mode
%attr(6050,root,yarn) %{_bindir}/container-executor

%changelog
* Wed Oct 23 2013 Robert Rati <rrati@redhat> - 2.2.0-1
- Update to upstream 2.2.0
- New patch to open libjvm with dlopen
- Conditionally compile libhdfs and deps for x86 only
- Added BR on objenesis >= 1.2-16
- Removed rpath from libhdfs
- Removed unneeded header files from devel
- Removed kfs removal patch

* Thu Oct 10 2013 Robert Rati <rrati@redhat> - 2.0.5-12
- Removed workaround for BZ1015612
- Filtered libhadoop provides/requires (BZ1017596)
- Fixed symlink for hdfs-bkjournal
- Moved libhdfs.so to devel package (BZ1017579)
- Fixed symlink paths for hadoop jars (BZ1017568)
- Added ownership of %{_datadir}/%{name}/hadoop/common

* Mon Oct  7 2013 Robert Rati <rrati@redhat> - 2.0.5-11
- Workaround for BZ1015612
- Added BuildRequires on gcc-g++ and make
- Removed duplicated deps from common package

* Thu Oct  3 2013 Robert Rati <rrati@redhat> - 2.0.5-10
- Added dependency on which
- Added pom files for test jars
- Removed workaround for BZ986909
- Packaged additional test jars and pom files
- Added workaround for bz1012059
- Updated hdfs-create-dirs to format the namenode if it is not formatted
- Spec cleanup

* Fri Sep 13 2013 Robert Rati <rrati@redhat> - 2.0.5-9
- Removed rcc.  It was obsolete and conflicted with qt-devel (BZ1003034)
- Moved to xmvn-subst for jar dependency symlinks
- Packaged test jars into test subpackage
- hdfs subpackage contains bkjounal jar
- Created client subpackage
- Moved libhdfs to %{_libdir} (BZ1003036)
- Added dependency from libhdfs to hdfs (BZ1003039)

* Wed Aug 28 2013 Robert Rati <rrati@redhat> - 2.0.5-8
- Removed systemPath, version, and scope from tools.jar dependency definition

* Tue Aug 20 2013 Robert Rati <rrati@redhat> - 2.0.5-7
- Changed hdfs subpackage from hadoop-libhdfs to libhdfs
- Don't build any packages on arm architectures

* Thu Aug 08 2013 Robert Rati <rrati@redhat> - 2.0.5-6
- Made libhdfs dependencies arch specific
- Moved docs into common

* Wed Aug 07 2013 Robert Rati <rrati@redhat> - 2.0.5-5
- Corrected license info
- Removed duplicate Requires
- Removed rpath references
- Corrected some permissions

* Tue Aug 06 2013 Robert Rati <rrati@redhat> - 2.0.5-4
- Native bits only built/packaged for intel architectures
- javadoc only generated on 64-bit intel
- Updated URL

* Wed Jul 24 2013 Robert Rati <rrati@redhat> - 2.0.5-3
- Removed gmaven as BR

* Wed Jul 24 2013 Robert Rati <rrati@redhat> - 2.0.5-2
- Fixed packaging for JNI jar/libraries
- Made packages noarch that are architecture independent
- Added cglib as a BuildRequires
- Removed explicit lib Requires
- Convert to XMvn macros
- Packaged the maven plugin
- Convert to jetty9 jspc compiler
- Removed xmlenc workaround

* Tue Jul 16 2013 Robert Rati <rrati@redhat> - 2.0.5-1
- Initial packaging
