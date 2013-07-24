%global _hardened_build 1

# Currently disabled because httpfs doesn't play well with the directory
# layout and isn't flexible enough to allow customization.
%global package_httpfs 0

%global commit b92d9bcf559cc2e62fc166e09bd2852766b27bec
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global hadoop_version %{version}-alpha
%global hdfs_services hadoop-zkfc.service hadoop-datanode.service hadoop-secondarynamenode.service hadoop-namenode.service
%global mapreduce_services hadoop-historyserver.service
%global yarn_services hadoop-proxyserver.service hadoop-resourcemanager.service hadoop-nodemanager.service
%global httpfs_services hadoop-httpfs.service

%define link_jars(d:f:)\
for pattern in %* \
do \
  for file in `%{_bindir}/build-classpath $pattern | tr ":" "\\n"` \
  do \
    %{__ln_s} $file %{buildroot}/%{-d*} \
    echo "%{-d*}/$(basename $file)" >> %{-f*} \
  done \
done \
%{nil}

Name:   hadoop
Version: 2.0.5
Release: 1%{?dist}
Summary: A software platform for processing vast amounts of data
License: ASL 2.0
Group:  Development/Libraries
URL: https://github.com/apache/hadoop-common.git
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
# https://issues.apache.org/jira/browse/HADOOP-9605
# https://issues.apache.org/jira/browse/HADOOP-9607
# https://issues.apache.org/jira/browse/HADOOP-9610
# https://issues.apache.org/jira/browse/HADOOP-9611
# https://issues.apache.org/jira/browse/HADOOP-9613
# https://issues.apache.org/jira/browse/HADOOP-9623
# https://issues.apache.org/jira/browse/HADOOP-9650
Patch0: hadoop-fedora-integration.patch
# Remove the kfs dependency (https://issues.apache.org/jira/browse/HADOOP-8886)
Patch1: hadoop-8886.patch
# Fedora packaging guidelines for JNI library loading
Patch2: hadoop-jni-library-loading.patch
# Clean up warnings with maven 3.0.5
Patch3: hadoop-maven.patch
# This is not a real BR, but is here because of rawhide shift to eclipse
# aether packages.
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
BuildRequires: cmake
BuildRequires: commons-codec
BuildRequires: commons-httpclient
%if package_httpfs
BuildRequires: ecj >= 1:4.2.1-6
%endif
BuildRequires: fuse-devel
BuildRequires: fusesource-pom
BuildRequires: geronimo-jms
BuildRequires: gcc-c++
BuildRequires: glassfish-jaxb
BuildRequires: glassfish-jsp
BuildRequires: glassfish-jsp-api
BuildRequires: gmaven
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
BuildRequires: jline
BuildRequires: jsch
BuildRequires: json_simple
BuildRequires: jsr-305
BuildRequires: jsr-311
BuildRequires: junit
BuildRequires: jzlib
BuildRequires: log4j
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
BuildRequires: objenesis
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
BuildRequires: tomcat-lib
BuildRequires: tomcat-servlet-3.0-api
BuildRequires: txw2
BuildRequires: xmlenc
BuildRequires: znerd-oss-parent
BuildRequires: zookeeper-java

# For tests
BuildRequires: jersey-test-framework
BuildRequires: maven-surefire-provider-junit4

%description
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

%package common
Summary: Common files needed by hadoop daemons
Group: Applications/System
BuildArch: noarch
Requires: /usr/sbin/useradd
Requires: antlr-tool
Requires: apache-commons-beanutils
Requires: apache-commons-cli
Requires: apache-commons-codec
Requires: apache-commons-collections
Requires: apache-commons-configuration
Requires: apache-commons-el
Requires: apache-commons-io
Requires: apache-commons-lang
Requires: apache-commons-logging
Requires: apache-commons-math
Requires: apache-commons-net
Requires: avalon-framework
Requires: avalon-logkit
Requires: avro
Requires: checkstyle
Requires: commons-httpclient
Requires: coreutils
Requires: geronimo-jms
Requires: glassfish-jaxb
Requires: glassfish-jsp
Requires: glassfish-jsp-api
Requires: guava
Requires: httpcomponents-client
Requires: httpcomponents-core
Requires: istack-commons
Requires: jackson
Requires: java
Requires: java-base64
Requires: java-xmlbuilder
Requires: javamail
Requires: jersey
Requires: jets3t
Requires: jettison
Requires: jetty-http
Requires: jetty-io
Requires: jetty-security
Requires: jetty-server
Requires: jetty-servlet
Requires: jetty-util
Requires: jetty-util-ajax
Requires: jetty-webapp
Requires: jetty-xml
Requires: jline
Requires: jsch
Requires: jsr-305
Requires: jsr-311
Requires: log4j
Requires: mockito
Requires: nc6
Requires: netty
Requires: objectweb-asm
Requires: objenesis
Requires: paranamer
Requires: protobuf-java
Requires: relaxngDatatype
Requires: servlet3
Requires: slf4j
Requires: snappy-java
Requires: tomcat-servlet-3.0-api
Requires: tomcat-el-2.2-api
Requires: txw2
Requires: xmlenc
Requires: zookeeper-java

%description common
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains common files and utilities needed by other Hadoop modules.

%package common-native
Summary: The native Hadoop library file
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}

%description common-native
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains the native-hadoop library

%package devel
Summary: Headers for Hadoop
Group: Development/System
BuildArch: noarch
Requires: %{name}-libhdfs = %{version}-%{release}

%description devel
Header files for Hadoop's libhdfs library and other utilities

%package hdfs
Summary: The Hadoop Distributed File System
Group: Applications/System
BuildArch: noarch
Requires: %{name}-common = %{version}-%{release}
Requires(pre): %{name}-common = %{version}-%{release}
Requires: apache-commons-daemon
Requires: apache-commons-daemon-jsvc
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description hdfs
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

The Hadoop Distributed File System (HDFS) is the primary storage system
used by Hadoop applications.

%package hdfs-fuse
Summary: Allows mounting of Hadoop HDFS
Group: Development/Libraries
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libhdfs = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: fuse

%description hdfs-fuse
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides tools that allow HDFS to be mounted as a standard
file system through fuse.

%if %{package_httpfs}
%package httpfs
Summary: Provides web access to HDFS
Group: Applications/System
BuildArch: noarch
Requires: %{name}-hdfs = %{version}-%{release}
Requires: apache-commons-dbcp
Requires: ecj >= 1:4.2.1-6
Requires: tomcat
Requires: tomcat-lib
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description httpfs
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides a server that provides HTTP REST API support for
the complete FileSystem/FileContext interface in HDFS.
%endif

%package javadoc
Summary: Javadoc for Hadoop
Group: Documentation
BuildArch: noarch

%description javadoc
This package contains the API documentation for %{name}

%package libhdfs
Summary: The Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
Requires: lzo

%description libhdfs
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides the Hadoop Filesystem Library.

%package mapreduce
Summary: Hadoop MapReduce (MRv2)
Group: Applications/System
BuildArch: noarch
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description mapreduce
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides Hadoop MapReduce (MRv2).

%package mapreduce-examples
Summary: Hadoop MapReduce (MRv2) examples
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
Requires: java

%description maven-plugin
The Hadoop maven plugin

%package yarn
Summary: Hadoop YARN
Group: Applications/System
BuildArch: noarch
Requires: %{name}-common = %{version}-%{release}
Requires(pre): %{name}-common = %{version}-%{release}
Requires: aopalliance
Requires: atinject
Requires: google-guice
Requires: guice-servlet
Requires: hamcrest
Requires: jersey-contribs
Requires: junit
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description yarn
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains Hadoop YARN.

%package yarn-security
Summary: The ability to run Hadoop YARN in secure mode
Group: Applications/System
Requires: %{name}-yarn = %{version}-%{release}

%description yarn-security
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.  YARN (Hadoop NextGen MapReduce) is
a general purpose data-computation framework.

This package contains files needed to run Hadoop YARN in secure mode.

%prep
%setup -qn %{name}-common-%{commit}
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1

# The hadoop test suite needs classes from the zookeeper test suite.
# We need to modify the deps to use the pom for the zookeeper-test jar
%pom_remove_dep org.apache.zookeeper:zookeeper hadoop-common-project/hadoop-common
%pom_add_dep org.apache.zookeeper:zookeeper hadoop-common-project/hadoop-common
%pom_add_dep org.apache.zookeeper:zookeeper-test hadoop-common-project/hadoop-common
%pom_remove_dep org.apache.zookeeper:zookeeper hadoop-hdfs-project/hadoop-hdfs
%pom_add_dep org.apache.zookeeper:zookeeper hadoop-hdfs-project/hadoop-hdfs
%pom_add_dep org.apache.zookeeper:zookeeper-test hadoop-hdfs-project/hadoop-hdfs

# War files we don't want
%mvn_package org.apache.hadoop:hadoop-auth-examples __noinstall
%mvn_package org.apache.hadoop:hadoop-hdfs-httpfs __noinstall

# We don't want these jars either because they are empty
%mvn_package org.apache.hadoop:hadoop-assemblies __noinstall
%mvn_package org.apache.hadoop:hadoop-client __noinstall
%mvn_package org.apache.hadoop:hadoop-dist __noinstall
%mvn_package org.apache.hadoop:hadoop-minicluster __noinstall
%mvn_package org.apache.hadoop:hadoop-tools-dist __noinstall
%mvn_package org.apache.hadoop:hadoop-yarn-server-tests __noinstall

# Parts we don't want to distribute
%mvn_package :hadoop-hdfs-bkjournal __noinstall

# Create separate file lists for packaging
%mvn_package ":%{name}-hdfs*" hadoop-hdfs
%mvn_package ":%{name}-mapreduce-client*" hadoop-mapreduce
%mvn_package ":%{name}-archives*" hadoop-mapreduce
%mvn_package ":%{name}-datajoin*" hadoop-mapreduce
%mvn_package ":%{name}-distcp*" hadoop-mapreduce
%mvn_package ":%{name}-extras*" hadoop-mapreduce
%mvn_package ":%{name}-gridmix*" hadoop-mapreduce
%mvn_package ":%{name}-rumen*" hadoop-mapreduce
%mvn_package ":%{name}-streaming*" hadoop-mapreduce
%mvn_package ":%{name}-mapreduce-examples*" hadoop-mapreduce-examples
%mvn_package ":%{name}-maven-plugins" hadoop-maven-plugin
%mvn_package ":%{name}-yarn*" hadoop-yarn

# Workaround for BZ986909
%mvn_package :%{name}-common __noinstall

# Jar files for common
# Workaround for BZ986909
#%%mvn_file ":%{name}-common" %{_jnidir}/%{name}-common %{_datadir}/%{name}/common/%{name}-common
%mvn_file ":{%{name}-{annotations,auth}}" %{name}/@1 %{_datadir}/%{name}/common/lib/@1

# Jar files for hdfs
%mvn_file ":%{name}-hdfs" %{name}/%{name}-hdfs %{_datadir}/%{name}/hdfs/%{name}-hdfs

# Jar files for mapreduce
%mvn_file ":{%{name}-mapreduce-client-*}" %{name}/@1 %{_datadir}/%{name}/mapreduce/@1
%mvn_file ":{%{name}-{archives,datajoin,distcp,extras,gridmix,rumen,streaming}}" %{name}/@1 %{_datadir}/%{name}/mapreduce/@1

# Jar files for mapreduce-examples
%mvn_file ":%{name}-mapreduce-examples" %{name}/%{name}-mapreduce-examples %{_datadir}/%{name}/mapreduce/%{name}-mapreduce-examples

# Jar files for yarn
%mvn_file ":{%{name}-yarn-*}" %{name}/@1 %{_datadir}/%{name}/yarn/@1

%build
%mvn_build -- -Drequire.snappy=true -Dcontainer-executor.conf.dir=%{_sysconfdir}/hadoop -Pdist,native -DskipTests -DskipTest -DskipIT

# This takes a long time to run, so comment out for now
#%%check
#mvn-rpmbuild -Pdist,native test -Dmaven.test.failure.ignore=true

%install
%mvn_install

install -d -m 0755 %{buildroot}/%{_libdir}/%{name}
install -d -m 0755 %{buildroot}/%{_includedir}/%{name}
install -d -m 0755 %{buildroot}/%{_jnidir}/
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{name}-hdfs/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/common/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/hdfs/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/yarn/lib
install -d -m 0755 %{buildroot}/%{_sysconfdir}/%{name}/tomcat
install -d -m 0755 %{buildroot}/%{_sysconfdir}/logrotate.d
install -d -m 0755 %{buildroot}/%{_tmpfilesdir}
install -d -m 1777 %{buildroot}/%{_var}/cache/%{name}-yarn
install -d -m 1777 %{buildroot}/%{_var}/cache/%{name}-hdfs
install -d -m 1777 %{buildroot}/%{_var}/cache/%{name}-mapreduce
install -d -m 0775 %{buildroot}/%{_var}/log/%{name}-yarn
install -d -m 0775 %{buildroot}/%{_var}/log/%{name}-hdfs
install -d -m 0775 %{buildroot}/%{_var}/log/%{name}-mapreduce
install -d -m 0775 %{buildroot}/%{_var}/run/%{name}-yarn
install -d -m 0775 %{buildroot}/%{_var}/run/%{name}-hdfs
install -d -m 0775 %{buildroot}/%{_var}/run/%{name}-mapreduce
%if %{package_httpfs}
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/bin
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/lib
install -d -m 0755 %{buildroot}/%{_libexecdir}/%{name}-httpfs
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{name}-httpfs/webapps
install -d -m 0775 %{buildroot}/%{_var}/log/%{name}-httpfs
install -d -m 0775 %{buildroot}/%{_var}/run/%{name}-httpfs
%endif

basedir='hadoop-dist/target/hadoop-%{hadoop_version}'

for dir in bin libexec sbin
do
  cp -arf $basedir/$dir %{buildroot}/%{_prefix}
done

# We don't care about this
rm -f %{buildroot}/%{_bindir}/test-container-executor

# Duplicate files
rm -f %{buildroot}/%{_sbindir}/hdfs-config.sh

cp -arf $basedir/etc %{buildroot}
cp -arf $basedir/include/* %{buildroot}/%{_includedir}/%{name}
cp -arf $basedir/lib/native/*.so* %{buildroot}/%{_libdir}/%{name}
cp -af hadoop-hdfs-project/hadoop-hdfs/target/native/main/native/fuse-dfs/fuse_dfs %{buildroot}/%{_bindir}

%if 0%{package_httpfs} == 0
rm -f %{buildroot}/%{_sbindir}/httpfs.sh
rm -f %{buildroot}/%{_libexecdir}/httpfs-config.sh
rm -f %{buildroot}/%{_sysconfdir}/%{name}/httpfs*
%endif

# Modify hadoop-env.sh to point to correct locations for JAVA_HOME
# and JSVC_HOME.
sed -i "s|\${JAVA_HOME}|/usr/lib/jvm/jre|" %{buildroot}/%{_sysconfdir}/%{name}/hadoop-env.sh
sed -i "s|\${JSVC_HOME}|/usr/bin|" %{buildroot}/%{_sysconfdir}/%{name}/hadoop-env.sh

# Ensure the java provided DocumentBuilderFactory is used
sed -i "s|\(HADOOP_OPTS.*=.*\)\$HADOOP_CLIENT_OPTS|\1 -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl \$HADOOP_CLIENT_OPTS|" %{buildroot}/%{_sysconfdir}/%{name}/hadoop-env.sh
echo "export YARN_OPTS=\"\$YARN_OPTS -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl\"" >> %{buildroot}/%{_sysconfdir}/%{name}/yarn-env.sh

# Workaround for BZ986909
# hadoop-common uses JNI so needs to be handled separately
cp -arf $basedir/share/hadoop/common/%{name}-common-%{hadoop_version}.jar %{buildroot}/%{_jnidir}/%{name}-common.jar
pushd %{buildroot}/%{_datadir}/%{name}/common
  %{__ln_s} %{_jnidir}/%{name}-common.jar .
popd
install -pm 664 hadoop-common-project/hadoop-common/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-common.pom
%add_maven_depmap JPP-%{name}-common.pom %{name}-common.jar -f hadoop-common

# common jar depenencies
%link_jars -d %{_datadir}/%{name}/common/lib -f .mfiles antlr objectweb-asm/asm avalon-framework-api avalon-logkit avro/avro base64 cglib checkstyle commons-beanutils-core commons-cli commons-codec commons-collections commons-configuration commons-el commons-httpclient commons-io commons-lang commons-logging commons-math3 commons-net guava httpcomponents/httpclient httpcomponents/httpcore istack-commons-runtime jackson/jackson-core-asl jackson/jackson-jaxrs jackson/jackson-mapper-asl jackson/jackson-xc java-xmlbuilder tomcat-servlet-api glassfish-jsp glassfish-jsp-api glassfish-jaxb/jaxb-impl jersey/jersey-core jersey/jersey-json jersey/jersey-server jersey/jersey-servlet jets3t/jets3t jettison jetty/jetty-http jetty/jetty-io jetty/jetty-security jetty/jetty-server jetty/jetty-servlet jetty/jetty-util jetty/jetty-util-ajax jetty/jetty-webapp jetty/jetty-xml jline jms jsch jsr-305 jsr-311 jzlib log4j javamail/mail mockito netty objenesis paranamer/paranamer protobuf relaxngDatatype slf4j/api slf4j/log4j12 snappy-java tomcat/tomcat-el-2.2-api txw2 xmlenc zookeeper/zookeeper

# hdfs jar dependencies
%link_jars -d %{_datadir}/%{name}/hdfs/lib -f .mfiles-hadoop-hdfs antlr objectweb-asm/asm avalon-framework-api avalon-logkit cglib checkstyle commons-beanutils-core commons-cli commons-codec commons-daemon commons-io commons-lang commons-logging guava jackson/jackson-core-asl jackson/jackson-mapper-asl tomcat-servlet-api jersey/jersey-core jersey/jersey-server jetty/jetty-http jetty/jetty-io jetty/jetty-server jetty/jetty-util jline jms jsr-311 jzlib log4j javamail/mail mockito netty objenesis protobuf slf4j/api xmlenc zookeeper/zookeeper

%if %{package_httpfs}
# httpfs
cp -arf $basedir/share/hadoop/httpfs/tomcat/bin/*.sh %{buildroot}/%{_libexecdir}/%{name}-httpfs
cp -arf $basedir/share/hadoop/httpfs/tomcat/bin/catalina-tasks.xml %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/bin
cp -arf $basedir/share/hadoop/httpfs/tomcat/conf/* %{buildroot}/%{_sysconfdir}/%{name}/tomcat
cp -arf $basedir/share/hadoop/httpfs/tomcat/webapps %{buildroot}/%{_sharedstatedir}/%{name}-httpfs
pushd %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat
  %{_bindir}/build-jar-repository -s bin tomcat/tomcat-juli commons-daemon
  %{_bindir}/build-jar-repository -s lib tomcat/annotations-api tomcat/catalina-ant tomcat/catalina-ha tomcat/catalina tomcat/catalina-tribes ecj tomcat/tomcat-el-2.2-api tomcat/jasper-el tomcat/jasper glassfish-jsp-api tomcat-servlet-api tomcat/tomcat-coyote commons-dbcp tomcat/tomcat-i18n-es tomcat/tomcat-i18n-fr tomcat/tomcat-i18n-ja
  %{__ln_s} %{_datadir}/tomcat/bin/bootstrap.jar bin
  for f in `ls %{buildroot}/%{_libexecdir}/%{name}-httpfs`
  do
    %{__ln_s} %{_libexecdir}/%{name}-httpfs/$f bin
  done
  %{__ln_s} %{_sysconfdir}/%{name}/tomcat conf 
  %{__ln_s} %{_var}/log/%{name}-httpfs logs
  %{__ln_s} %{_sharedstatedir}/%{name}-httpfs/webapps webapps
  %{__ln_s} %{_var}/cache/%{name}-httpfs/temp temp
  %{__ln_s} %{_var}/cache/%{name}-httpfs/work work
popd
%endif

# mapreduce jar dependencies
%link_jars -d %{_datadir}/%{name}/mapreduce/lib -f .mfiles-hadoop-mapreduce aopalliance atinject objectweb-asm/asm avro/avro commons-io guava google-guice guice/guice-servlet %{name}/%{name}-annotations hamcrest/core jackson/jackson-core-asl jackson/jackson-mapper-asl jersey/jersey-core jersey/jersey-guice jersey/jersey-server jersey/jersey-servlet jsr-311 junit jzlib log4j netty paranamer/paranamer protobuf snappy-java

# yarn jar dependencies
%link_jars -d %{_datadir}/%{name}/yarn/lib -f .mfiles-hadoop-yarn aopalliance atinject objectweb-asm/asm avro/avro cglib commons-io guava google-guice guice/guice-servlet %{name}/%{name}-annotations hamcrest/core jackson/jackson-core-asl jackson/jackson-mapper-asl jersey/jersey-core jersey/jersey-guice jersey/jersey-server jersey/jersey-servlet jsr-311 junit jzlib log4j netty paranamer/paranamer protobuf snappy-java

# Install hdfs webapp bits
cp -arf $basedir/share/hadoop/hdfs/webapps %{buildroot}/%{_sharedstatedir}/%{name}-hdfs
pushd %{buildroot}/%{_datadir}/%{name}/hdfs
  %{__ln_s} %{_sharedstatedir}/%{name}-hdfs/webapps webapps
popd

# hadoop layout. Convert to appropriate lib location for 32 and 64 bit archs
lib=$(echo %{?_libdir} | sed -e 's:/usr/\(.*\):\1:')
if [ "$lib" = "%_libdir" ]; then
  echo "_libdir is not located in /usr.  Lib location is wrong"
  exit 1
fi
sed -e "s|HADOOP_COMMON_LIB_NATIVE_DIR\s*=.*|HADOOP_COMMON_LIB_NATIVE_DIR=$lib/%{name}|" %{SOURCE1} > %{buildroot}/%{_libexecdir}/hadoop-layout.sh

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
%endif

# Install security limits
install -d -m 0755 %{buildroot}/%{_sysconfdir}/security/limits.d
for limit in hdfs yarn mapreduce
do
  sed -e "s|name|${limit:0:6}|" %{SOURCE7} > %{buildroot}/%{_sysconfdir}/security/limits.d/${limit}.conf
done

# Ensure /var/run directories are recreated on boot
echo "d %{_var}/run/%{name}-yarn 0775 yarn hadoop -" > %{buildroot}/%{_tmpfilesdir}/hadoop-yarn.conf
echo "d %{_var}/run/%{name}-hdfs 0775 hdfs hadoop -" > %{buildroot}/%{_tmpfilesdir}/hadoop-hdfs.conf
echo "d %{_var}/run/%{name}-mapreduce 0775 mapred hadoop -" > %{buildroot}/%{_tmpfilesdir}/hadoop-mapreduce.conf
%if %{package_httpfs}
echo "d %{_var}/run/%{name}-httpfs 0775 httpfs hadoop -" > %{buildroot}/%{_tmpfilesdir}/hadoop-httpfs.conf
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

%pre common
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HDFS" --shell /sbin/nologin -M -r -g hdfs -G hadoop --home %{_var}/cache/%{name}-hdfs hdfs

%if %{package_httpfs}
%pre httpfs 
getent group httpfs >/dev/null || groupadd -r httpfs
getent passwd httpfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HTTPFS" --shell /sbin/nologin -M -r -g httpfs -G httpfs --home %{_var}/run/%{name}-httpfs httpfs
%endif

%pre mapreduce
getent group mapred >/dev/null || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Hadoop MapReduce" --shell /sbin/nologin -M -r -g mapred -G hadoop --home %{_var}/cache/%{name}-mapreduce mapred

%pre yarn
getent group yarn >/dev/null || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Hadoop Yarn" --shell /sbin/nologin -M -r -g yarn -G hadoop --home %{_var}/cache/%{name}-yarn yarn

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

%post common -p /sbin/ldconfig

%post hdfs
%systemd_post %{hdfs_services}

%if %{package_httpfs}
%post httpfs
%systemd_post %{httpfs_services}
%endif

%post libhdfs -p /sbin/ldconfig

%post mapreduce
%systemd_post %{mapreduce_services}

%post yarn
%systemd_post %{yarn_services}

%postun common -p /sbin/ldconfig

%postun hdfs
%systemd_postun_with_restart %{hdfs_services}

%if %{package_httpfs}
%postun httpfs
%systemd_postun_with_restart %{httpfs_services}
%endif

%postun libhdfs -p /sbin/ldconfig

%postun mapreduce
%systemd_postun_with_restart %{mapreduce_services}

%postun yarn
%systemd_postun_with_restart %{yarn_services}

%files -f .mfiles common
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/LICENSE.txt
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
%{_datadir}/%{name}/common/%{name}-common.jar
# Workaround for BZ986909
%{_jnidir}/%{name}-common.jar
%{_libexecdir}/%{name}-config.sh
%{_libexecdir}/%{name}-layout.sh
%{_mavenpomdir}/JPP-%{name}-common.pom
%{_mavendepmapfragdir}/%{name}-%{name}-common
%{_bindir}/%{name}
%{_bindir}/rcc
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

%files devel
%{_includedir}/%{name}

%files -f .mfiles-hadoop-hdfs hdfs
%config(noreplace) %{_sysconfdir}/%{name}/hdfs-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/hdfs.conf
%dir %{_datadir}/%{name}/hdfs
%{_datadir}/%{name}/hdfs/webapps
%{_sharedstatedir}/%{name}-hdfs
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

%files hdfs-fuse
%{_bindir}/fuse_dfs

%if %{package_httpfs}
%files httpfs
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-log4j.properties
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-signature.secret
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/tomcat
%{_libexecdir}/httpfs-config.sh
%{_libexecdir}/%{name}-httpfs
%{_unitdir}/%{name}-httpfs.service
%{_sbindir}/httpfs.sh
%{_datadir}/%{name}/httpfs
%{_sharedstatedir}/%{name}-httpfs
%{_tmpfilesdir}/%{name}-httpfs.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-httpfs
%attr(0755,httpfs,httpfs) %dir %{_var}/run/%{name}-httpfs
%attr(0755,httpfs,httpfs) %dir %{_var}/log/%{name}-httpfs
%endif

%files -f .mfiles-javadoc javadoc
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/*

%files libhdfs
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/hdfs/LICENSE.txt
%{_libdir}/%{name}/libhdfs*

%files -f .mfiles-hadoop-mapreduce mapreduce
%config(noreplace) %{_sysconfdir}/%{name}/mapred-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/mapred-queues.xml.template
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml.template
%config(noreplace) %{_sysconfdir}/security/limits.d/mapreduce.conf
%dir %{_datadir}/%{name}/mapreduce
%{_libexecdir}/mapred-config.sh
%{_unitdir}/%{name}-historyserver.service
%{_bindir}/mapred
%{_sbindir}/mr-jobhistory-daemon.sh
%{_tmpfilesdir}/%{name}-mapreduce.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/run/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/log/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/cache/%{name}-mapreduce

%files -f .mfiles-hadoop-mapreduce-examples mapreduce-examples

%files -f .mfiles-hadoop-maven-plugin maven-plugin
%doc hadoop-dist/target/hadoop-%{hadoop_version}/share/doc/hadoop/common/LICENSE.txt

%files -f .mfiles-hadoop-yarn yarn
%config(noreplace) %{_sysconfdir}/%{name}/capacity-scheduler.xml
%config(noreplace) %{_sysconfdir}/%{name}/yarn-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/yarn-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/yarn.conf
%{_unitdir}/%{name}-nodemanager.service
%{_unitdir}/%{name}-proxyserver.service
%{_unitdir}/%{name}-resourcemanager.service
%{_libexecdir}/yarn-config.sh
%dir %{_datadir}/%{name}/yarn
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
* Tue Jul 16 2013 Robert Rati <rrati@redhat> - 2.0.5-1
- Initial packaging
