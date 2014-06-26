%global _hardened_build 1

# libhdfs is only supported on intel architectures atm.
%ifarch %ix86 x86_64
%global package_libhdfs 1
%else
%global package_libhdfs 0
%endif

%global commit 9d04888c2ca6ffc0d11e5fd894e3fa567398214a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global hadoop_version %{version}
%global hdfs_services hadoop-zkfc.service hadoop-datanode.service hadoop-secondarynamenode.service hadoop-namenode.service hadoop-journalnode.service
%global mapreduce_services hadoop-historyserver.service
%global yarn_services hadoop-proxyserver.service hadoop-resourcemanager.service hadoop-nodemanager.service hadoop-timelineserver.service

# Filter out undesired provides and requires
%global __requires_exclude_from ^%{_libdir}/%{name}/libhadoop.so$
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$

%bcond_with javadoc

Name:   hadoop
Version: 2.4.0
Release: 3%{?dist}
Summary: A software platform for processing vast amounts of data
# The BSD license file is missing
# https://issues.apache.org/jira/browse/HADOOP-9849
License: ASL 2.0 and BSD
URL: http://hadoop.apache.org
Source0: https://github.com/apache/hadoop-common/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1: %{name}-layout.sh
Source2: %{name}-hdfs.service.template
Source3: %{name}-mapreduce.service.template
Source4: %{name}-yarn.service.template
Source6: %{name}.logrotate
Source8: %{name}-core-site.xml
Source9: %{name}-hdfs-site.xml
Source10: %{name}-mapred-site.xml
Source11: %{name}-yarn-site.xml
Source12: %{name}-httpfs.sysconfig
Source13: hdfs-create-dirs
Source14: %{name}-tomcat-users.xml
# This patch includes the following upstream tickets:
# https://issues.apache.org/jira/browse/HADOOP-9613
# https://issues.apache.org/jira/browse/HDFS-5411
# https://issues.apache.org/jira/browse/HADOOP-10068
# https://issues.apache.org/jira/browse/HADOOP-10075
# https://issues.apache.org/jira/browse/HADOOP-10076
Patch0: %{name}-fedora-integration.patch
# Fedora packaging guidelines for JNI library loading
Patch2: %{name}-jni-library-loading.patch
# Clean up warnings with maven 3.0.5
Patch3: %{name}-maven.patch
# Don't download tomcat
Patch4: %{name}-no-download-tomcat.patch
# Use dlopen to find libjvm.so
Patch5: %{name}-dlopen-libjvm.patch
# Update to Guava 17.0
Patch7: %{name}-guava.patch
# Update to Netty 3.6.6-Final
Patch8: %{name}-netty-3.6.6-Final.patch
# Remove problematic issues with tools.jar
Patch9: %{name}-tools.jar.patch
# Workaround for bz1012059
Patch10: %{name}-build.patch
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
BuildRequires: ecj >= 1:4.2.1-6
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
BuildRequires: hawtjni
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
BuildRequires: jetty8
BuildRequires: jsch
BuildRequires: json_simple
BuildRequires: jspc
BuildRequires: jsr-305
BuildRequires: jsr-311
BuildRequires: junit
BuildRequires: jzlib
BuildRequires: leveldbjni
%if 0%{?fedora} < 21
BuildRequires: log4j
%else
BuildRequires: log4j12
%endif
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
BuildRequires: metrics
BuildRequires: mockito
BuildRequires: native-maven-plugin
%if 0%{?fedora} < 21
BuildRequires: netty
%else
BuildRequires: netty3
%endif
%if 0%{?fedora} > 20
BuildRequires: objectweb-asm3
%else
BuildRequires: objectweb-asm
%endif
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
BuildRequires: tomcat
BuildRequires: tomcat-el-2.2-api
%if 0%{?fedora} > 20
BuildRequires: tomcat-log4j
%endif
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: txw2
BuildRequires: which
BuildRequires: xmlenc
BuildRequires: znerd-oss-parent
%if 0%{?fedora} < 21
BuildRequires: zookeeper-java
%else
BuildRequires: zookeeper-java > 3.4.5-15
%endif

# For tests
BuildRequires: jersey-test-framework
%if 0%{?fedora} > 20
BuildRequires: maven-surefire-provider-junit
%else
BuildRequires: maven-surefire-provider-junit4
%endif

%description
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

%package client
Summary: Libraries for Apache Hadoop clients
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
Requires: java-base64
Requires: java-xmlbuilder
Requires: javamail
Requires: jettison
Requires: jetty8
Requires: jsr-311
Requires: mockito
Requires: nc6
%if 0%{?fedora} > 20
Requires: objectweb-asm3
%else
Requires: objectweb-asm
%endif
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
Requires: libhdfs%{?_isa} = %{version}-%{release}

%description devel
Header files for Apache Hadoop's hdfs library and other utilities
%endif

%package hdfs
Summary: The Apache Hadoop Distributed File System
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

%package httpfs
Summary: Provides web access to HDFS
BuildArch: noarch
Requires: apache-commons-dbcp
Requires: ecj >= 1:4.2.1-6
Requires: json_simple
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

# Creation of javadocs takes too many resources and results in failures  on
# most architectures so only generate on intel 64-bit
%ifarch x86_64
%if %{with javadoc}
%package javadoc
Summary: Javadoc for Apache Hadoop
BuildArch: noarch

%description javadoc
This package contains the API documentation for %{name}.
%endif
%endif

%if %{package_libhdfs}
%package -n libhdfs
Summary: The Apache Hadoop Filesystem Library
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
BuildArch: noarch
Requires(pre): %{name}-common = %{version}-%{release}
Requires(pre): %{name}-yarn = %{version}-%{release}
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
BuildArch: noarch
Requires: hsqldb

%description mapreduce-examples
This package contains mapreduce examples.

%package maven-plugin
Summary: Apache Hadoop maven plugin
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
BuildArch: noarch
Requires(pre): %{name}-common = %{version}-%{release}
Requires: aopalliance
Requires: atinject
Requires: hamcrest
Requires: hawtjni
Requires: leveldbjni
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
%patch4 -p1
%if %{package_libhdfs}
%patch5 -p1
%endif
%if 0%{?fedora} >= 21
%patch7 -p1
%patch8 -p1
%endif
%patch9 -p1
%patch10 -p1

%if 0%{?fedora} < 21
# The hadoop test suite needs classes from the zookeeper test suite.
# We need to modify the deps to use the pom for the zookeeper-test jar
fix_zookeeper_test()
{
%pom_xpath_remove "pom:project/pom:dependencies/pom:dependency[pom:artifactId='zookeeper' and pom:scope='test']/pom:type" $1 
%pom_xpath_inject "pom:project/pom:dependencies/pom:dependency[pom:artifactId='zookeeper' and pom:scope='test']" " 
      <exclusions>
        <exclusion>
          <groupId>org.jboss.netty</groupId>
          <artifactId>netty</artifactId>
        </exclusion>
      </exclusions>
  " $1
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:artifactId='zookeeper' and pom:scope='test']/pom:artifactId" zookeeper-test $1 
}

fix_zookeeper_test hadoop-common-project/hadoop-common
fix_zookeeper_test hadoop-hdfs-project/hadoop-hdfs
fix_zookeeper_test hadoop-hdfs-project/hadoop-hdfs-nfs
fix_zookeeper_test hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager

sed -i "s/:pom//" hadoop-yarn-project/hadoop-yarn/hadoop-yarn-client/pom.xml
fix_zookeeper_test hadoop-yarn-project/hadoop-yarn/hadoop-yarn-client
%endif

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

# Disable the hadoop-minikdc module due to missing deps
%pom_disable_module hadoop-minikdc hadoop-common-project
%pom_remove_dep :hadoop-minikdc hadoop-common-project/hadoop-auth
%pom_remove_dep :hadoop-minikdc hadoop-project
%pom_remove_dep :hadoop-minikdc hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-tests
rm -f hadoop-common-project/hadoop-auth/src/test/java/org/apache/hadoop/security/authentication/client/TestKerberosAuthenticator.java
rm -f hadoop-common-project/hadoop-auth/src/test/java/org/apache/hadoop/security/authentication/server/TestKerberosAuthenticationHandler.java
rm -f hadoop-common-project/hadoop-auth/src/test/java/org/apache/hadoop/security/authentication/server/TestAltKerberosAuthenticationHandler.java
rm -f hadoop-common-project/hadoop-auth/src/test/java/org/apache/hadoop/security/authentication/server/TestKerberosAuthenticationHandler.java
rm -f hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-tests/src/test/java/org/apache/hadoop/yarn/server/TestContainerManagerSecurity.java

# Add dependencies for timeline service
%pom_add_dep org.iq80.leveldb:leveldb hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-applicationhistoryservice
%pom_add_dep org.fusesource.hawtjni:hawtjni-runtime hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-applicationhistoryservice

# Fix scope on hadoop-common:test-jar
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:artifactId='hadoop-common' and pom:type='test-jar']/pom:scope" test hadoop-tools/hadoop-openstack

# Modify asm version to version 5.0.2
%pom_xpath_set "pom:project/pom:dependencyManagement/pom:dependencies/pom:dependency[pom:artifactId='asm']/pom:version" 5.0.2 hadoop-project

# War files we don't want
%mvn_package :%{name}-auth-examples __noinstall
%mvn_package :%{name}-hdfs-httpfs __noinstall

# Parts we don't want to distribute
%mvn_package :%{name}-assemblies __noinstall

# Workaround for bz1012059
%mvn_package :%{name}-project-dist __noinstall

# Create separate file lists for packaging
%mvn_package :::tests: %{name}-tests
%mvn_package :%{name}-*-tests::{}: %{name}-tests
%mvn_package :%{name}-client*::{}: %{name}-client
%mvn_package :%{name}-hdfs*::{}: %{name}-hdfs
%mvn_package :%{name}-mapreduce-examples*::{}: %{name}-mapreduce-examples
%mvn_package :%{name}-mapreduce*::{}: %{name}-mapreduce
%mvn_package :%{name}-archives::{}: %{name}-mapreduce
%mvn_package :%{name}-datajoin::{}: %{name}-mapreduce
%mvn_package :%{name}-distcp::{}: %{name}-mapreduce
%mvn_package :%{name}-extras::{}: %{name}-mapreduce
%mvn_package :%{name}-gridmix::{}: %{name}-mapreduce
%mvn_package :%{name}-openstack::{}: %{name}-mapreduce
%mvn_package :%{name}-rumen::{}: %{name}-mapreduce
%mvn_package :%{name}-sls::{}: %{name}-mapreduce
%mvn_package :%{name}-streaming::{}: %{name}-mapreduce
%mvn_package :%{name}-pipes::{}: %{name}-mapreduce
%mvn_package :%{name}-tools*::{}: %{name}-mapreduce
%mvn_package :%{name}-maven-plugins::{}: %{name}-maven-plugin
%mvn_package :%{name}-minicluster::{}: %{name}-tests
%mvn_package :%{name}-yarn*::{}: %{name}-yarn

# Jar files that need to be overridden due to installation location
%mvn_file :%{name}-common::tests: %{name}/%{name}-common

%build
%ifnarch x86_64
opts="-j"
%else
%if %{without javadoc}
opts="-j"
%endif
%endif
%mvn_build $opts -- -Drequire.snappy=true -Dcontainer-executor.conf.dir=%{_sysconfdir}/%{name} -Pdist,native -DskipTests -DskipTest -DskipIT

# This takes a long time to run, so comment out for now
#%%check
#mvn-rpmbuild -Pdist,native test -Dmaven.test.failure.ignore=true

%install
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

# Create symlinks for jars from the build
# $1 the location to create the symlink
link_hadoop_jars()
{
  for f in `ls hadoop-* | grep -v tests | grep -v examples`
  do
    n=`echo $f | sed "s/-%{version}//"`
    if [ -L $1/$n ]
    then
      continue
    elif [ -e $1/$f ]
    then
      rm -f $1/$f $1/$n
    fi
    p=`find %{buildroot}/%{_jnidir} %{buildroot}/%{_javadir}/%{name} -name $n | sed "s#%{buildroot}##"`
    %{__ln_s} $p $1/$n
  done
}

%mvn_install

install -d -m 0755 %{buildroot}/%{_libdir}/%{name}
install -d -m 0755 %{buildroot}/%{_includedir}/%{name}
install -d -m 0755 %{buildroot}/%{_jnidir}/%{name}

install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/client/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/common/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/hdfs/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/hdfs/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/yarn/lib
install -d -m 0755 %{buildroot}/%{_sysconfdir}/%{name}/tomcat/Catalina/localhost
install -d -m 0755 %{buildroot}/%{_sysconfdir}/logrotate.d
install -d -m 0755 %{buildroot}/%{_sysconfdir}/sysconfig
install -d -m 0755 %{buildroot}/%{_tmpfilesdir}
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{name}-hdfs
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/tomcats/httpfs
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-httpfs/temp
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-httpfs/work
install -d -m 0755 %{buildroot}/%{_var}/cache/%{name}-mapreduce
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-hdfs
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-httpfs
install -d -m 0755 %{buildroot}/%{_var}/log/%{name}-mapreduce
install -d -m 0755 %{buildroot}/%{_var}/run/%{name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/run/%{name}-hdfs
install -d -m 0755 %{buildroot}/%{_var}/run/%{name}-mapreduce

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

# Not needed since httpfs is deployed with existing systemd setup
rm -f %{buildroot}/%{_sbindir}/httpfs.sh
rm -f %{buildroot}/%{_libexecdir}/httpfs-config.sh
rm -f %{buildroot}/%{_bindir}/httpfs-env.sh

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
install -pm 644 hadoop-project-dist/pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}-%{name}-project-dist.pom
%{__ln_s} %{_jnidir}/%{name}/hadoop-common.jar %{buildroot}/%{_datadir}/%{name}/common
#echo %{_datadir}/%{name}/common/hadoop-common.jar >> .mfiles
%{__ln_s} %{_javadir}/%{name}/hadoop-hdfs.jar %{buildroot}/%{_datadir}/%{name}/hdfs
echo %{_datadir}/%{name}/hdfs/hadoop-hdfs.jar >> .mfiles-%{name}-hdfs
%{__ln_s} %{_javadir}/%{name}/hadoop-client.jar %{buildroot}/%{_datadir}/%{name}/client
echo %{_datadir}/%{name}/client/hadoop-client.jar >> .mfiles-%{name}-client

# client jar depenencies
copy_dep_jars %{name}-client/target/%{name}-client-%{hadoop_version}/share/%{name}/client/lib %{buildroot}/%{_datadir}/%{name}/client/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/client/lib
pushd  %{name}-client/target/%{name}-client-%{hadoop_version}/share/%{name}/client/lib
  link_hadoop_jars %{buildroot}/%{_datadir}/%{name}/client/lib
popd
pushd  %{name}-client/target/%{name}-client-%{hadoop_version}/share/%{name}/client
  link_hadoop_jars %{buildroot}/%{_datadir}/%{name}/client
popd

# common jar depenencies
copy_dep_jars $basedir/share/%{name}/common/lib %{buildroot}/%{_datadir}/%{name}/common/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/common/lib
pushd $basedir/share/%{name}/common
  link_hadoop_jars %{buildroot}/%{_datadir}/%{name}/common
popd
for f in `ls %{buildroot}/%{_datadir}/%{name}/common/*.jar`
do
  echo "$f" | sed "s|%{buildroot}||" >> .mfiles
done
pushd $basedir/share/%{name}/common/lib
  link_hadoop_jars %{buildroot}/%{_datadir}/%{name}/common/lib
popd

# hdfs jar dependencies
copy_dep_jars $basedir/share/%{name}/hdfs/lib %{buildroot}/%{_datadir}/%{name}/hdfs/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/hdfs/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-hdfs-bkjournal.jar %{buildroot}/%{_datadir}/%{name}/hdfs/lib
pushd $basedir/share/%{name}/hdfs
  link_hadoop_jars %{buildroot}/%{_datadir}/%{name}/hdfs
popd

# httpfs
# Create the webapp directory structure
pushd %{buildroot}/%{_sharedstatedir}/tomcats/httpfs
  %{__ln_s} %{_datadir}/%{name}/httpfs/tomcat/conf conf
  %{__ln_s} %{_datadir}/%{name}/httpfs/tomcat/lib lib
  %{__ln_s} %{_datadir}/%{name}/httpfs/tomcat/logs logs
  %{__ln_s} %{_datadir}/%{name}/httpfs/tomcat/temp temp
  %{__ln_s} %{_datadir}/%{name}/httpfs/tomcat/webapps webapps
  %{__ln_s} %{_datadir}/%{name}/httpfs/tomcat/work work
popd

# Copy the tomcat configuration and overlay with specific configuration bits.
# This is needed so the httpfs instance won't collide with a system running
# tomcat
for f in catalina.policy catalina.properties context.xml log4j.properties \
         tomcat.conf web.xml;
do
  cp -a %{_sysconfdir}/tomcat/$f %{buildroot}/%{_sysconfdir}/%{name}/tomcat
done

install -m 660 %{SOURCE14} %{buildroot}/%{_sysconfdir}/%{name}/tomcat/tomcat-users.xml
install -m 664 %{name}-hdfs-project/%{name}-hdfs-httpfs/src/main/tomcat/*.* %{buildroot}/%{_sysconfdir}/%{name}/tomcat

# Copy the httpfs webapp
cp -arf %{name}-hdfs-project/%{name}-hdfs-httpfs/target/webhdfs %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/webapps

# Tell tomcat to follow symlinks
cat > %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/webapps/webhdfs/META-INF/context.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<Context allowLinking="true">
</Context>
EOF

# Remove the jars included in the webapp and create symlinks
rm -f %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib/tools*.jar
rm -f %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib/tomcat-*.jar
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib
pushd %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib
  link_hadoop_jars .
popd

pushd %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat
  %{__ln_s} %{_datadir}/tomcat/bin bin
  %{__ln_s} %{_sysconfdir}/%{name}/tomcat conf
  %{__ln_s} %{_datadir}/tomcat/lib lib
  %{__ln_s} %{_var}/cache/%{name}-httpfs/temp temp
  %{__ln_s} %{_var}/cache/%{name}-httpfs/work work
  %{__ln_s} %{_var}/log/%{name}-httpfs logs
popd

# mapreduce jar dependencies
copy_dep_jars $basedir/share/%{name}/mapreduce/lib %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-annotations.jar %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
pushd $basedir/share/%{name}/mapreduce
  link_hadoop_jars %{buildroot}/%{_datadir}/%{name}/mapreduce
popd

# yarn jar dependencies
copy_dep_jars $basedir/share/%{name}/yarn/lib %{buildroot}/%{_datadir}/%{name}/yarn/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{name}/yarn/lib
%{__ln_s} %{_javadir}/%{name}/%{name}-annotations.jar %{buildroot}/%{_datadir}/%{name}/yarn/lib
pushd $basedir/share/%{name}/yarn
  link_hadoop_jars %{buildroot}/%{_datadir}/%{name}/yarn
popd

# Install hdfs webapp bits
cp -arf $basedir/share/hadoop/hdfs/webapps/* %{buildroot}/%{_datadir}/%{name}/hdfs/webapps

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
  daemon=$s
  if [[ "%{hdfs_services}" == *$service* ]]
  then
    src=%{SOURCE2}
  elif [[ "%{mapreduce_services}" == *$service* ]]
  then
    src=%{SOURCE3}
  elif [[ "%{yarn_services}" == *$service* ]]
  then
    if [[ "$s" == "timelineserver" ]]
    then
      daemon='historyserver'
    fi
    src=%{SOURCE4}
  else
    echo "Failed to determine type of service for %service"
    exit 1
  fi
  sed -e "s|DAEMON|$daemon|g" $src > %{buildroot}/%{_unitdir}/%{name}-$s.service
done

cp -f %{SOURCE12} %{buildroot}/%{_sysconfdir}/sysconfig/tomcat@httpfs

# Ensure /var/run directories are recreated on boot
echo "d %{_var}/run/%{name}-yarn 0775 yarn hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{name}-yarn.conf
echo "d %{_var}/run/%{name}-hdfs 0775 hdfs hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{name}-hdfs.conf
echo "d %{_var}/run/%{name}-mapreduce 0775 mapred hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{name}-mapreduce.conf

# logrotate config
for type in hdfs httpfs yarn mapreduce
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

%pretrans -p <lua> hdfs
path = "%{_datadir}/%{name}/hdfs/webapps"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%pre common
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop HDFS" --shell /sbin/nologin -M -r -g hdfs -G hadoop --home %{_sharedstatedir}/%{name}-hdfs hdfs

%pre mapreduce
getent group mapred >/dev/null || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop MapReduce" --shell /sbin/nologin -M -r -g mapred -G hadoop --home %{_var}/cache/%{name}-mapreduce mapred

%pre yarn
getent group yarn >/dev/null || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop Yarn" --shell /sbin/nologin -M -r -g yarn -G hadoop --home %{_var}/cache/%{name}-yarn yarn

%preun hdfs
%systemd_preun %{hdfs_services}

%preun mapreduce
%systemd_preun %{mapreduce_services}

%preun yarn
%systemd_preun %{yarn_services}

%post common-native -p /sbin/ldconfig

%post hdfs
# Change the home directory for the hdfs user
if [[ `getent passwd hdfs | cut -d: -f 6` != "%{_sharedstatedir}/%{name}-hdfs" ]]
then
  /usr/sbin/usermod -d %{_sharedstatedir}/%{name}-hdfs hdfs
fi

if [ $1 -gt 1 ]
then
  if [ -d %{_var}/cache/%{name}-hdfs ] && [ ! -L %{_var}/cache/%{name}-hdfs ]
  then
    # Move the existing hdfs data to the new location
    mv -f %{_var}/cache/%{name}-hdfs/* %{_sharedstatedir}/%{name}-hdfs/
  fi
fi
%systemd_post %{hdfs_services}

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

if [ $1 -lt 1 ]
then
  # Remove the compatibility symlink
  rm -f %{_var}/cache/%{name}-hdfs
fi

%if %{package_libhdfs}
%postun -n libhdfs -p /sbin/ldconfig
%endif

%postun mapreduce
%systemd_postun_with_restart %{mapreduce_services}

%postun yarn
%systemd_postun_with_restart %{yarn_services}

%posttrans hdfs
# Create a symlink to the new location for hdfs data in case the user changed
# the configuration file and the new one isn't in place to point to the
# correct location
if [ ! -e %{_var}/cache/%{name}-hdfs ]
then
  %{__ln_s} %{_sharedstatedir}/%{name}-hdfs %{_var}/cache
fi

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
%{_datadir}/%{name}/common/lib
%{_libexecdir}/%{name}-config.sh
%{_libexecdir}/%{name}-layout.sh

# Workaround for bz1012059
%{_mavenpomdir}/JPP.%{name}-%{name}-project-dist.pom

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
%config(noreplace) %{_sysconfdir}/%{name}/hdfs-site.xml
%{_datadir}/%{name}/hdfs
%{_unitdir}/%{name}-datanode.service
%{_unitdir}/%{name}-namenode.service
%{_unitdir}/%{name}-journalnode.service
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
%attr(0755,hdfs,hadoop) %dir %{_sharedstatedir}/%{name}-hdfs

%if %{package_libhdfs}
%files hdfs-fuse
%attr(755,hdfs,hadoop) %{_bindir}/fuse_dfs
%endif

%files httpfs
%config(noreplace) %{_sysconfdir}/sysconfig/tomcat@httpfs
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-log4j.properties
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-signature.secret
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-site.xml
%attr(-,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{name}/tomcat/*.*
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{name}/tomcat
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{name}/tomcat/Catalina
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{name}/tomcat/Catalina/localhost
%{_datadir}/%{name}/httpfs
%{_sharedstatedir}/tomcats/httpfs
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/log/%{name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/cache/%{name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/cache/%{name}-httpfs/temp
%attr(0775,root,tomcat) %dir %{_var}/cache/%{name}-httpfs/work

%ifarch x86_64
%if %{with javadoc}
%files -f .mfiles-javadoc javadoc
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/LICENSE.txt hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/NOTICE.txt
%endif
%endif

%if %{package_libhdfs}
%files -n libhdfs
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/hdfs/LICENSE.txt
%{_libdir}/libhdfs.so.*
%endif

%files -f .mfiles-%{name}-mapreduce mapreduce
%config(noreplace) %{_sysconfdir}/%{name}/mapred-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/mapred-queues.xml.template
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml.template
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
%config(noreplace) %{_sysconfdir}/%{name}/capacity-scheduler.xml
%config(noreplace) %{_sysconfdir}/%{name}/yarn-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/yarn-site.xml
%{_unitdir}/%{name}-nodemanager.service
%{_unitdir}/%{name}-proxyserver.service
%{_unitdir}/%{name}-resourcemanager.service
%{_unitdir}/%{name}-timelineserver.service
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
* Thu Jun 26 2014 Robert Rati <rrati@redhat> - 2.4.0-3
- Fixed FTBFS (#1106748)
- Update to build with guava 17.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Robert Rati <rrati@redhat> - 2.4.0-1
- Update to upstream release 2.4.0
- Fix fedora conditionals for non-fedora systems (BZ1083135)
- Conditionalize javadoc generation
- Update BuildRequires

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.0-7
- Use Requires: java-headless rebuild (#1067528)

* Mon Feb 17 2014 Timothy St. Clair <tstclair@redhat.com> - 2.2.0-6
- Rebuild with modification to systemd initialization for tachyon support

* Mon Feb  3 2014 Robert Rati <rrati@redhat> - 2.2.0-5
- Added json_simple dependency to httpfs package
- Added default tomcat-users file
- Fixed up file permissions and ownership for tomcat configuration
- Conditionalize the zookeeper-test modes to < F21
- Additional fix for netty3 compat package for >F20

* Fri Jan 24 2014 Robert Rati <rrati@redhat> - 2.2.0-4
- Fixed 2 packages providing hadoop-yarn-server-tests (BZ1056521)
- Package httpfs bits using tomcat@ service
- Patches for jetty 9.1.0 and guava 0.15 on >F20
- Use netty3 compat package for >F20
- Moved limits configuration to systemd files
- By default logrotate will keep 1 year of logs

* Tue Dec  3 2013 Robert Rati <rrati@redhat> - 2.2.0-3
- Removed jline Requires

* Tue Dec  3 2013 Robert Rati <rrati@redhat> - 2.2.0-2
- Changed provides filter to just filter the .so
- Corrected naming of hadoop-common test jar
- Removed jline BuildRequires
- Moved pre/port install invocation of ldconfig to common-native
- Added workaround for bz1023116

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
