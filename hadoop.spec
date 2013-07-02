# Currently disabled because httpfs doesn't play well with the directory
# layout and isn't flexible enough to allow customization.
%global package_httpfs 0

%global commit 812b8ce7e062eb480e1114738bf9b267f46b3c73
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global hadoop_base_version 2.0.2-alpha
%global hdfs_services hadoop-zkfc.service hadoop-datanode.service hadoop-secondarynamenode.service hadoop-namenode.service
%global mapreduce_services hadoop-historyserver.service
%global yarn_services hadoop-proxyserver.service hadoop-resourcemanager.service hadoop-nodemanager.service
%global httpfs_services hadoop-httpfs.service

Name:   hadoop
Version: 2.0.2
Release: 1%{?dist}
Summary: A software platform for processing vast amounts of data
License: ASL 2.0
Group:  Development/Libraries
URL: https://github.com/apache/hadoop-common.git
#Source0: %{name}-%{hadoop_base_version}.tar.gz
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
# As well as still baking changes for tomcat/jspc
Patch0: hadoop-fedora-integration.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)
BuildRequires: ant
BuildRequires: apache-commons-cli
BuildRequires: apache-commons-configuration
BuildRequires: apache-commons-daemon
BuildRequires: apache-commons-el
BuildRequires: apache-commons-io
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-logging
BuildRequires: apache-commons-math
BuildRequires: apache-commons-net
BuildRequires: apache-rat-plugin
BuildRequires: avro
BuildRequires: bookkeeper-java
BuildRequires: cmake
BuildRequires: commons-codec
BuildRequires: commons-httpclient
BuildRequires: ecj >= 1:4.2.1-6
BuildRequires: fuse
BuildRequires: fuse-devel
BuildRequires: fusesource-pom
BuildRequires: gmaven
BuildRequires: grizzly
BuildRequires: guava
BuildRequires: guice-servlet
BuildRequires: guice-extensions
BuildRequires: hsqldb
BuildRequires: jackson
BuildRequires: jansi
BuildRequires: jansi-native
BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: jdiff
BuildRequires: jersey
BuildRequires: jersey-contribs
BuildRequires: jets3t
# May need to break down into specific jetty rpms
BuildRequires: jetty
BuildRequires: jsch
BuildRequires: json_simple
BuildRequires: jspc
BuildRequires: jspc-compilers
BuildRequires: jspc-maven-plugin
BuildRequires: junit
BuildRequires: kfs
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
BuildRequires: openssl-devel
BuildRequires: protobuf-compiler
BuildRequires: protobuf-java
BuildRequires: servlet3
BuildRequires: slf4j
BuildRequires: snappy
BuildRequires: snappy-devel
BuildRequires: systemd
BuildRequires: tomcat-lib
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
Requires: /usr/sbin/useradd
Requires: apache-commons-cli
Requires: apache-commons-codec
Requires: apache-commons-configuration
Requires: apache-commons-el
Requires: apache-commons-io
Requires: apache-commons-lang
Requires: apache-commons-logging
Requires: apache-commons-math
Requires: apache-commons-net
Requires: avro
Requires: commons-httpclient
Requires: coreutils
Requires: ecj >= 1:4.2.1-6
Requires: glassfish-jaxb
Requires: glassfish-jsp
Requires: glassfish-jsp-api
Requires: guava
Requires: hawtjni
Requires: httpcomponents-client
Requires: httpcomponents-core
Requires: istack-commons
Requires: jackson
Requires: jansi
Requires: jansi-native
Requires: java
Requires: java-base64
Requires: java-xmlbuilder
Requires: jersey
Requires: jets3t
Requires: jettison
Requires: jetty-continuation
Requires: jetty-http
Requires: jetty-io
Requires: jetty-security
Requires: jetty-server
Requires: jetty-servlet
Requires: jetty-util
Requires: jetty-webapp
Requires: jetty-xml
Requires: jline
Requires: jsch
Requires: jsr-311
Requires: kfs
Requires: log4j
Requires: nc6
Requires: netty
Requires: objectweb-asm
Requires: paranamer
Requires: protobuf-java
Requires: relaxngDatatype
Requires: servlet3
Requires: slf4j
Requires: snappy-java
Requires: tomcat-el-2.2-api
Requires: txw2
Requires: xmlenc
Requires: zookeeper-java

%description common
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.  The hadoop-common package contains
common files and utilities needed by other Hadoop modules.

%package devel
Summary: Headers for Hadoop
Group: Development/System
Requires: %{name}-libhdfs = %{version}-%{release}

%description devel
Header files for Hadoop's libhdfs library and other utilities

%package hdfs
Summary: The Hadoop Distributed File System
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires(pre): %{name}-common = %{version}-%{release}
Requires: apache-commons-daemon
Requires: apache-commons-daemon-jsvc
%systemd_requires

%description hdfs
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.  The Hadoop Distributed File System
(HDFS) is the primary storage system used by Hadoop applications.

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
offering local computation and storage.  This package provides tools that
allow HDFS to be mounted as a standard file system through fuse.

%if %{package_httpfs}
%package httpfs
Summary: Provides web access to HDFS
Group: Applications/System
Requires: %{name}-hdfs = %{version}-%{release}
Requires: apache-commons-dbcp
Requires: tomcat
Requires: tomcat-lib
%systemd_requires

%description httpfs
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.  This package provides a server
that provides HTTP REST API support for the complete FileSystem/FileContext
interface in HDFS.
%endif

%package javadoc
Summary: Javadoc for Hadoop
Group: Documentation
Requires: jpackage-utils

%description javadoc
This package contains the API documentation for %{name}

%package libhdfs
Summary: The Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
Requires: lzo
Requires: zlib

%description libhdfs
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.  This package provides the Hadoop
Filesystem Library

%package mapreduce
Summary: Hadoop MapReduce (MRv2)
Group: Applications/System
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name}-common = %{version}-%{release}
%systemd_requires

%description mapreduce
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.  Hadoop MapReduce is a programming
model and software framework for writing applications that rapidly process vast
amounts of data in parallel on large clusters of compute nodes.

%package mapreduce-examples
Summary: Hadoop MapReduce (MRv2) examples
Group: Applications/System
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: hsqldb

%description mapreduce-examples
This package contains mapreduce examples.

%package yarn
Summary: Hadoop YARN
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires(pre): %{name}-common = %{version}-%{release}
Requires: aopalliance
Requires: atinject
Requires: cglib
Requires: google-guice
Requires: guice-servlet
Requires: hamcrest
Requires: jersey-contribs
Requires: junit
%systemd_requires

%description yarn
Hadoop is a framework that allows for the distributed processing of large data
sets across clusters of computers using simple programming models.  It is
designed to scale up from single servers to thousands of machines, each
offering local computation and storage.  YARN (Hadoop NextGen MapReduce) is
a general purpose data-computation framework.

%prep
#%%setup -qn %{name}-%{hadoop_base_version}
%setup -qn %{name}-common-%{commit}
%patch0 -p1

# The hadoop test suite needs classes from the zookeeper test suite.
# We need to modify the deps to use the pom for the zookeeper-test jar
%pom_remove_dep org.apache.zookeeper:zookeeper hadoop-common-project/hadoop-common
%pom_add_dep org.apache.zookeeper:zookeeper hadoop-common-project/hadoop-common
%pom_add_dep org.apache.zookeeper:zookeeper-test hadoop-common-project/hadoop-common
%pom_remove_dep org.apache.zookeeper:zookeeper hadoop-hdfs-project/hadoop-hdfs
%pom_add_dep org.apache.zookeeper:zookeeper hadoop-hdfs-project/hadoop-hdfs
%pom_add_dep org.apache.zookeeper:zookeeper-test hadoop-hdfs-project/hadoop-hdfs

%build
mvn-rpmbuild -Drequire.snappy=true -Pdist,native -DskipTests package javadoc:aggregate

%check
mvn-rpmbuild -Pdist,native test -Dmaven.test.failure.ignore=true

%clean
rm -rf %{buildroot}

%install
install -d -m 0755 %{buildroot}/%{_libdir}
install -d -m 0755 %{buildroot}/%{_includedir}/%{name}
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{name}-hdfs/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/common/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/hdfs/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/yarn/lib
install -d -m 0755 %{buildroot}/%{_javadir}/%{name}
install -d -m 0755 %{buildroot}/%{_javadocdir}/%{name}
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

basedir='hadoop-dist/target/hadoop-%{hadoop_base_version}'

for dir in bin libexec sbin
do
  cp -arf $basedir/$dir %{buildroot}/%{_prefix}
done

# We don't care about this
rm -f %{buildroot}/%{_bindir}/test-container-executor

cp -arf $basedir/etc %{buildroot}
cp -arf $basedir/include/* %{buildroot}/%{_includedir}/%{name}
cp -arf $basedir/lib/native/*.so* %{buildroot}/%{_libdir}
cp -af hadoop-hdfs-project/hadoop-hdfs/target/native/main/native/fuse-dfs/fuse_dfs %{buildroot}/%{_bindir}

for dir in `ls $basedir/share/hadoop`
do
  if [ $dir == "httpfs" ]
  then
    # We need to handle httpfs differently.  We don't want the jar files
    # (they are copies or incorrect versions), but do want other bits
    continue
  fi
  find $basedir/share/hadoop/$dir -name *-%{hadoop_base_version}.jar | xargs cp -af -t %{buildroot}/%{_javadir}/%{name}
done

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

# /usr/share file structure
for dir in common hdfs mapreduce yarn
do
  pushd %{buildroot}/%{_datadir}/%{name}/$dir
    for file in `ls %{buildroot}/%{_javadir}/%{name}/%{name}-$dir-*`
    do
      %{__ln_s} %{_javadir}/%{name}/$(basename $file) .
    done
  popd
done

pushd %{buildroot}/%{_datadir}/%{name}/common/lib
  %{__ln_s} %{_javadir}/%{name}/%{name}-annotations-%{hadoop_base_version}.jar .
  %{__ln_s} %{_javadir}/%{name}/%{name}-auth-%{hadoop_base_version}.jar .
  %{_bindir}/build-jar-repository -s . objectweb-asm/asm avro/avro base64 commons-cli commons-codec commons-configuration commons-el commons-httpclient commons-io commons-lang commons-logging commons-math3 commons-net ecj guava hawtjni-runtime httpcomponents/httpclient httpcomponents/httpcore istack-commons-runtime jackson/jackson-core-asl jackson/jackson-jaxrs jackson/jackson-mapper-asl jackson/jackson-xc jansi jansi-native java-xmlbuilder tomcat-servlet-api glassfish-jsp glassfish-jsp-api glassfish-jaxb/jaxb-impl jersey/jersey-core jersey/jersey-json jersey/jersey-server jersey/jersey-servlet jets3t/jets3t jettison jetty/jetty-continuation jetty/jetty-http jetty/jetty-io jetty/jetty-security jetty/jetty-server jetty/jetty-servlet jetty/jetty-util jetty/jetty-webapp jetty/jetty-xml jline jsch jsr-311 kfs log4j netty paranamer/paranamer protobuf relaxngDatatype slf4j/api slf4j/log4j12 snappy-java tomcat/tomcat-el-2.2-api txw2 xmlenc zookeeper
popd

pushd %{buildroot}/%{_datadir}/%{name}/hdfs/lib
  %{_bindir}/build-jar-repository -s . objectweb-asm/asm commons-cli commons-codec commons-daemon apache-commons-io commons-lang commons-logging guava hawtjni-runtime jackson/jackson-core-asl jackson/jackson-mapper-asl jansi jansi-native tomcat-servlet-api jersey/jersey-core jersey/jersey-server jetty/jetty-continuation jetty/jetty-http jetty/jetty-io jetty/jetty-server jetty/jetty-util jline jsr-311 log4j netty protobuf slf4j/api xmlenc zookeeper
popd

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

pushd %{buildroot}/%{_datadir}/%{name}/mapreduce
  %{__ln_s} %{_javadir}/%{name}/%{name}-archives-%{hadoop_base_version}.jar .
  %{__ln_s} %{_javadir}/%{name}/%{name}-datajoin-%{hadoop_base_version}.jar .
  %{__ln_s} %{_javadir}/%{name}/%{name}-distcp-%{hadoop_base_version}.jar .
  %{__ln_s} %{_javadir}/%{name}/%{name}-extras-%{hadoop_base_version}.jar .
  %{__ln_s} %{_javadir}/%{name}/%{name}-gridmix-%{hadoop_base_version}.jar .
  %{__ln_s} %{_javadir}/%{name}/%{name}-rumen-%{hadoop_base_version}.jar .
  %{__ln_s} %{_javadir}/%{name}/%{name}-streaming-%{hadoop_base_version}.jar .
popd

pushd %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
  %{__ln_s} %{_javadir}/%{name}/%{name}-annotations-%{hadoop_base_version}.jar .
  %{_bindir}/build-jar-repository -s . aopalliance atinject objectweb-asm/asm avro/avro apache-commons-io guava google-guice guice/guice-servlet hamcrest/core jackson/jackson-core-asl jackson/jackson-mapper-asl jersey/jersey-core jersey/jersey-guice jersey/jersey-server jersey/jersey-servlet jsr-311 junit log4j netty paranamer/paranamer protobuf snappy-java
popd

pushd %{buildroot}/%{_datadir}/%{name}/yarn/lib
  %{__ln_s} %{_javadir}/%{name}/%{name}-annotations-%{hadoop_base_version}.jar .
  %{_bindir}/build-jar-repository -s . aopalliance atinject objectweb-asm/asm avro/avro cglib apache-commons-io guava google-guice guice/guice-servlet hamcrest/core jackson/jackson-core-asl jackson/jackson-mapper-asl jersey/jersey-core jersey/jersey-guice jersey/jersey-server jersey/jersey-servlet jsr-311 junit log4j netty paranamer/paranamer protobuf snappy-java
popd

# Install hdfs webapp bits
cp -arf $basedir/share/hadoop/hdfs/webapps %{buildroot}/%{_sharedstatedir}/%{name}-hdfs
pushd %{buildroot}/%{_datadir}/%{name}/hdfs
  %{__ln_s} %{_sharedstatedir}/%{name}-hdfs/webapps webapps
popd

# javadocs
cp -arf target/site/apidocs/* %{buildroot}/%{_javadocdir}/%{name}

# hadoop layout. Convert to appropriate lib location for 32 and 64 bit archs
lib=$(echo %{?_libdir} | sed -e 's:/usr/\(.*\):\1:')
if [ "$lib" = "%_libdir" ]; then
  echo "_libdir is not located in /usr.  Lib location is wrong"
  exit 1
fi
sed -e "s|HADOOP_COMMON_LIB_NATIVE_DIR\s*=.*|HADOOP_COMMON_LIB_NATIVE_DIR=$lib|" %{SOURCE1} > %{buildroot}/%{_libexecdir}/hadoop-layout.sh

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
install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/security/limits.d
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
cp -arf %{SOURCE13} %{buildroot}/%{_sbindir}

install -dm 0775 %{buildroot}%{_mavenpomdir}
for module in hadoop-yarn-project/hadoop-yarn/hadoop-yarn-common \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-client \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-applications/hadoop-yarn-applications-unmanaged-am-launcher \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-applications/hadoop-yarn-applications-distributedshell \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-site \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-api \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-nodemanager \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-tests \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-web-proxy \
            hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-common \
            hadoop-common-project/hadoop-common \
            hadoop-common-project/hadoop-annotations \
            hadoop-common-project/hadoop-auth \
            hadoop-tools/hadoop-rumen hadoop-tools/hadoop-archives \
            hadoop-tools/hadoop-streaming hadoop-tools/hadoop-distcp \
            hadoop-tools/hadoop-extras hadoop-tools/hadoop-datajoin\
            hadoop-tools/hadoop-gridmix \
            hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-core \
            hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-app \
            hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-jobclient \
            hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-hs \
            hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-shuffle \
            hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-common \
            hadoop-mapreduce-project/hadoop-mapreduce-examples \
            hadoop-hdfs-project/hadoop-hdfs; do
  base=`basename $module`
  install -pm 644 $module/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-$base-%{hadoop_base_version}.pom
  %add_maven_depmap JPP.%{name}-$base-%{hadoop_base_version}.pom %{name}/$base-%{hadoop_base_version}.jar -f $base
done

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

%files common
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/configuration.xsl
%config(noreplace) %{_sysconfdir}/%{name}/core-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/hadoop-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/hadoop-metrics.properties
%config(noreplace) %{_sysconfdir}/%{name}/hadoop-metrics2.properties
%config(noreplace) %{_sysconfdir}/%{name}/log4j.properties
%config(noreplace) %{_sysconfdir}/%{name}/slaves
%config(noreplace) %{_sysconfdir}/%{name}/ssl-client.xml.example
%config(noreplace) %{_sysconfdir}/%{name}/ssl-server.xml.example
%{_javadir}/%{name}/%{name}-annotations*.jar
%{_javadir}/%{name}/%{name}-auth*.jar
%{_javadir}/%{name}/%{name}-common*.jar
%{_datadir}/%{name}/common
%{_mavenpomdir}/JPP.%{name}-%{name}-annotations*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-auth*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-common*.pom
%{_mavendepmapfragdir}/%{name}-%{name}-annotations*
%{_mavendepmapfragdir}/%{name}-%{name}-auth*
%{_mavendepmapfragdir}/%{name}-%{name}-common*
%{_libexecdir}/hadoop-config.sh
%{_libexecdir}/hadoop-layout.sh
%{_bindir}/hadoop
%{_bindir}/rcc
%{_sbindir}/hadoop-daemon.sh
%{_sbindir}/hadoop-daemons.sh
%{_sbindir}/hadoop-create-user.sh
%{_sbindir}/hadoop-setup-applications.sh
%{_sbindir}/hadoop-setup-conf.sh
%{_sbindir}/hadoop-setup-single-node.sh
%{_sbindir}/hadoop-validate-setup.sh
%{_sbindir}/start-all.sh
%{_sbindir}/start-balancer.sh
%{_sbindir}/start-dfs.sh
%{_sbindir}/start-secure-dns.sh
%{_sbindir}/stop-all.sh
%{_sbindir}/stop-balancer.sh
%{_sbindir}/stop-dfs.sh
%{_sbindir}/stop-secure-dns.sh
%{_sbindir}/slaves.sh
%{_sbindir}/update-hadoop-env.sh
%{_libdir}/libhadoop.*

%files devel
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%{_includedir}/%{name}

%files hdfs
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/hdfs/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/hdfs-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/hdfs.conf
%{_javadir}/%{name}/%{name}-hdfs*.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-hdfs*.pom
%{_mavendepmapfragdir}/%{name}-%{name}-hdfs*
%{_datadir}/%{name}/hdfs
%{_sharedstatedir}/%{name}-hdfs
%{_unitdir}/%{name}-datanode.service
%{_unitdir}/%{name}-namenode.service
%{_unitdir}/%{name}-secondarynamenode.service
%{_unitdir}/%{name}-zkfc.service
%{_libexecdir}/hdfs-config.sh
%{_bindir}/hdfs
%{_sbindir}/distribute-exclude.sh
%{_sbindir}/refresh-namenodes.sh
%{_sbindir}/hadoop-setup-hdfs.sh
%{_sbindir}/hdfs-config.sh
%{_sbindir}/hdfs-create-dirs
%{_sbindir}/update-hdfs-env.sh
%{_tmpfilesdir}/hadoop-hdfs.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/run/%{name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/log/%{name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/cache/%{name}-hdfs

%files hdfs-fuse
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/hdfs/*
%defattr(-,root,root)
%{_bindir}/fuse_dfs

%if %{package_httpfs}
%files httpfs
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-log4j.properties
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-signature.secret
%config(noreplace) %{_sysconfdir}/%{name}/httpfs-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/tomcat
%{_libexecdir}/httpfs-config.sh
%{_libexecdir}/%{name}-httpfs
%{_unitdir}/%{name}-httpfs.service
%{_sbindir}/httpfs.sh
%{_datadir}/hadoop/httpfs
%{_sharedstatedir}/hadoop-httpfs
%{_tmpfilesdir}/hadoop-httpfs.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-httpfs
%attr(0755,httpfs,httpfs) %dir %{_var}/run/%{name}-httpfs
%attr(0755,httpfs,httpfs) %dir %{_var}/log/%{name}-httpfs
%endif

%files javadoc
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%doc %{_javadocdir}/%{name}

%files libhdfs
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/hdfs/*
%defattr(-,root,root)
%{_libdir}/libhdfs*

%files mapreduce
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/mapreduce/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/mapred-env.sh
#%config(noreplace) %{_sysconfdir}/%{name}/mapred-queues.xml
%config(noreplace) %{_sysconfdir}/%{name}/mapred-queues.xml.template
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml.template
%config(noreplace) %{_sysconfdir}/security/limits.d/mapreduce.conf
%{_datadir}/%{name}/mapreduce
%{_javadir}/%{name}/%{name}-mapreduce-client*.jar
%{_javadir}/%{name}/%{name}-archives*.jar
%{_javadir}/%{name}/%{name}-datajoin*.jar
%{_javadir}/%{name}/%{name}-distcp*.jar
%{_javadir}/%{name}/%{name}-extras*.jar
%{_javadir}/%{name}/%{name}-gridmix*.jar
%{_javadir}/%{name}/%{name}-rumen*.jar
%{_javadir}/%{name}/%{name}-streaming*.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-mapreduce-client*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-archives*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-datajoin*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-distcp*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-extras*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-gridmix*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-rumen*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-streaming*.pom
%{_mavendepmapfragdir}/%{name}-%{name}-mapreduce-client*
%{_mavendepmapfragdir}/%{name}-%{name}-archives*
%{_mavendepmapfragdir}/%{name}-%{name}-datajoin*
%{_mavendepmapfragdir}/%{name}-%{name}-distcp*
%{_mavendepmapfragdir}/%{name}-%{name}-extras*
%{_mavendepmapfragdir}/%{name}-%{name}-gridmix*
%{_mavendepmapfragdir}/%{name}-%{name}-rumen*
%{_mavendepmapfragdir}/%{name}-%{name}-streaming*
%{_libexecdir}/mapred-config.sh
%{_unitdir}/%{name}-historyserver.service
%{_bindir}/mapred
%{_sbindir}/mr-jobhistory-daemon.sh
%{_tmpfilesdir}/hadoop-mapreduce.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/run/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/log/%{name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/cache/%{name}-mapreduce

%files mapreduce-examples
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/mapreduce/*
%{_javadir}/%{name}/%{name}-mapreduce-examples*.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-mapreduce-examples*.pom
%{_mavendepmapfragdir}/%{name}-%{name}-mapreduce-examples*

%files yarn
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/yarn/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/container-executor.cfg
%config(noreplace) %{_sysconfdir}/%{name}/yarn-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/yarn-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/yarn.conf
%{_unitdir}/%{name}-nodemanager.service
%{_unitdir}/%{name}-proxyserver.service
%{_unitdir}/%{name}-resourcemanager.service
%{_libexecdir}/yarn-config.sh
%{_javadir}/%{name}/%{name}-yarn*.jar
%{_datadir}/%{name}/yarn
%{_mavenpomdir}/JPP.%{name}-%{name}-yarn*.pom
%{_mavendepmapfragdir}/%{name}-%{name}-yarn*
%attr(6050,root,yarn) %{_bindir}/container-executor
%{_bindir}/yarn
%{_sbindir}/yarn-daemon.sh
%{_sbindir}/yarn-daemons.sh
%{_sbindir}/start-yarn.sh
%{_sbindir}/stop-yarn.sh
%{_tmpfilesdir}/hadoop-yarn.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/run/%{name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/log/%{name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/cache/%{name}-yarn

%changelog

