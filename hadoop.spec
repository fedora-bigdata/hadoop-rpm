# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Currently disabled because httpfs doesn't play well with the directory
# layout and isn't flexible enough to allow customization.
%global package_httpfs 0

%global hadoop_base_version 2.0.2-alpha
%global hdfs_services hadoop-zkfc.service hadoop-datanode.service hadoop-secondarynamenode.service hadoop-namenode.service
%global mapreduce_services hadoop-historyserver.service
%global yarn_services hadoop-proxyserver.service hadoop-resourcemanager.service hadoop-nodemanager.service
%global httpfs_services hadoop-httpfs.service

Name:   hadoop
Version: 2.0.2
Release: 0.1%{?dist}
Summary: Hadoop is a software platform for processing vast amounts of data
License: Apache License v2.0
URL:    http://hadoop.apache.org/core/
Group:  Development/Libraries
Source0: %{name}-%{hadoop_base_version}.tar.gz
Source1: hadoop-layout.sh
Source2: hadoop-hdfs.service.template
Source3: hadoop-mapreduce.service.template
Source4: hadoop-yarn.service.template
Source5: hadoop-httpfs.service
Source6: hadoop-datanode.sysconfig
Source7: hadoop-limits.conf
Source8: hadoop-core-site.xml
Source9: hadoop-hdfs-site.xml
Source10: hadoop-mapred-site.xml
Source11: hadoop-yarn-site.xml
Source12: hadoop-httpfs-env.sh
Patch0: hadoop-fedora-integration.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)
BuildRequires: systemd
BuildRequires: maven-compiler-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-invoker-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-cobertura
BuildRequires: maven-plugin-plugin
BuildRequires: maven-release-plugin
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-clean-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-shade-plugin
BuildRequires: maven-antrun-plugin
BuildRequires: apache-rat-plugin
BuildRequires: maven-plugin-exec
BuildRequires: native-maven-plugin
BuildRequires: znerd-oss-parent
BuildRequires: jspc-maven-plugin
BuildRequires: jspc-compilers
BuildRequires: gmaven
BuildRequires: fusesource-pom
BuildRequires: json_simple
BuildRequires: grizzly
BuildRequires: openssl-devel
BuildRequires: jspc
# May need to break down into specific jetty rpms
BuildRequires: jetty
BuildRequires: maven
BuildRequires: javapackages-tools
BuildRequires: fuse-devel
BuildRequires: fuse
BuildRequires: cmake
BuildRequires: protobuf-compiler
BuildRequires: jetty
BuildRequires: jersey
BuildRequires: java-devel
BuildRequires: junit
BuildRequires: mockito
BuildRequires: slf4j
BuildRequires: servlet3
BuildRequires: commons-codec
BuildRequires: apache-commons-cli
BuildRequires: apache-commons-math
BuildRequires: log4j
BuildRequires: guava
BuildRequires: commons-httpclient
BuildRequires: apache-commons-io
BuildRequires: apache-commons-net
BuildRequires: tomcat-lib
BuildRequires: apache-commons-el
BuildRequires: apache-commons-logging
BuildRequires: jets3t
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-configuration
BuildRequires: apache-commons-daemon
BuildRequires: jackson
BuildRequires: avro
BuildRequires: kfs
BuildRequires: ant
BuildRequires: protobuf-java
BuildRequires: jsch
BuildRequires: zookeeper-java
BuildRequires: xmlenc
BuildRequires: bookkeeper-java
BuildRequires: netty
BuildRequires: guice-servlet
BuildRequires: guice-extensions
BuildRequires: jersey-contribs
BuildRequires: jersey-test-framework
BuildRequires: grizzly
BuildRequires: jdiff
BuildRequires: ecj >= 4.2.1-6
BuildRequires: hsqldb
BuildRequires: snappy-devel
BuildRequires: snappy
BuildRequires: jansi
BuildRequires: jansi-native

# For tests
BuildRequires: maven-surefire-provider-junit4

Requires: coreutils
Requires: /usr/sbin/useradd
Requires: /usr/sbin/usermod
Requires: /sbin/chkconfig
Requires: /sbin/service
Requires: zookeeper
Requires: psmisc
Requires: nc6
#Requires: jersey
Requires: snappy-java
Requires: slf4j
Requires: netty
Requires: paranamer
Requires: protobuf-java
Requires: xmlenc
Requires: objectweb-asm
Requires: avro
Requires: apache-commons-beanutils
Requires: apache-commons-cli
Requires: apache-commons-codec
Requires: apache-commons-collections
Requires: apache-commons-configuration
Requires: apache-commons-digester
Requires: apache-commons-el
Requires: apache-commons-io
Requires: apache-commons-lang
Requires: apache-commons-logging
Requires: apache-commons-math
Requires: apache-commons-net
Requires: commons-httpclient
Requires: guava
Requires: jackson
Requires: glassfish-jaxb
Requires: glassfish-jaxb-api
Requires: jets3t
Requires: jettison
#Requires: jetty
Requires: jline
Requires: jsch
Requires: glassfish-jsp-api
Requires: jsr-305
Requires: kfs
Requires: log4j

%description
Hadoop is a software platform that lets one easily write and
run applications that process vast amounts of data.

Here's what makes Hadoop especially useful:
* Scalable: Hadoop can reliably store and process petabytes.
* Economical: It distributes the data and processing across clusters
              of commonly available computers. These clusters can number
              into the thousands of nodes.
* Efficient: By distributing the data, Hadoop can process it in parallel
             on the nodes where the data is located. This makes it
             extremely rapid.
* Reliable: Hadoop automatically maintains multiple copies of data and
            automatically redeploys computing tasks based on failures.

Hadoop implements MapReduce, using the Hadoop Distributed File System (HDFS).
MapReduce divides applications into many small blocks of work. HDFS creates
multiple replicas of data blocks for reliability, placing them on compute
nodes around the cluster. MapReduce can then process the data where it is
located.

%package hdfs
Summary: The Hadoop Distributed File System
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires: apache-commons-daemon-jsvc
Requires: jetty
%systemd_requires

%description hdfs
Hadoop Distributed File System (HDFS) is the primary storage system used by 
Hadoop applications. HDFS creates multiple replicas of data blocks and
distributes them on compute nodes throughout a cluster to enable reliable,
extremely rapid computations.

%package yarn
Summary: The Hadoop NextGen MapReduce (YARN)
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires: guice
Requires: avro
Requires: jersey
Requires: cglib
Requires: atinject
Requires: aopalliance
Requires: jsr-311
Requires: cglib
Requires: jackson
%systemd_requires

%description yarn
YARN (Hadoop NextGen MapReduce) is a general purpose data-computation framework.
The fundamental idea of YARN is to split up the two major functionalities of
the JobTracker, resource management and job scheduling/monitoring, into
separate daemons: ResourceManager and NodeManager.

The ResourceManager is the ultimate authority that arbitrates resources among
all the applications in the system. The NodeManager is a per-node slave
managing allocation of computational resources on a single node. Both work in
support of per-application ApplicationMaster (AM).

An ApplicationMaster is, in effect, a framework specific library and is tasked
with negotiating resources from the ResourceManager and working with the
NodeManager(s) to execute and monitor the tasks. 


%package mapreduce
Summary: The Hadoop MapReduce (MRv2)
Group: System/Daemons
Requires: %{name}-yarn = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
%systemd_requires

%description mapreduce
Hadoop MapReduce is a programming model and software framework for writing
applications that rapidly process vast amounts of data in parallel on large
clusters of compute nodes.

%if %{package_httpfs}
%package httpfs
Summary: HTTPFS for Hadoop
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}
Requires: tomcat
%systemd_requires

%description httpfs
The server providing HTTP REST API support for the complete
FileSystem/FileContext interface in HDFS.
%endif

%package libhdfs
Summary: Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
Requires: zlib
Requires: lzo

%description libhdfs
Hadoop Filesystem Library

%package hdfs-fuse
Summary: Mountable HDFS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libhdfs = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: fuse
Requires: fuse-libs

%description hdfs-fuse
Allow HDFS to be mounted as a standard file system

%package javadoc
Summary: Javadoc for %{name}
Group: Documentation
Requires: jpackage-utils

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{hadoop_base_version}-src
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
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{name}-hdfs/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/common/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/hdfs/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/mapreduce/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{name}/yarn/lib
install -d -m 0755 %{buildroot}/%{_javadir}/%{name}
install -d -m 0755 %{buildroot}/%{_javadocdir}/%{name}
install -d -m 0755 %{buildroot}/%{_sysconfdir}/sysconfig
install -d -m 0755 %{buildroot}/%{_sysconfdir}/%{name}/tomcat
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
  %{_bindir}/build-jar-repository -s . objectweb-asm/asm avro/avro commons-cli commons-codec commons-configuration commons-el commons-httpclient commons-io commons-lang commons-logging commons-math3 commons-net ecj guava hawtjni-runtime httpcomponents/httpclient httpcomponents/httpcore istack-commons-runtime jackson/jackson-core-asl jackson/jackson-jaxrs jackson/jackson-mapper-asl jackson/jackson-xc jansi jansi-native java-xmlbuilder tomcat-servlet-api glassfish-jsp glassfish-jsp-api glassfish-jaxb/jaxb-impl jersey/jersey-core jersey/jersey-json jersey/jersey-server jersey/jersey-servlet jets3t/jets3t jettison jetty/jetty-continuation jetty/jetty-http jetty/jetty-io jetty/jetty-security jetty/jetty-server jetty/jetty-servlet jetty/jetty-util jetty/jetty-webapp jetty/jetty-xml jline jsch jsr-311 kfs log4j netty paranamer/paranamer protobuf relaxngDatatype slf4j/api slf4j/log4j12 snappy-java tomcat/tomcat-el-2.2-api txw2 xmlenc zookeeper
popd

pushd %{buildroot}/%{_datadir}/%{name}/hdfs/lib
  %{_bindir}/build-jar-repository -s . objectweb-asm/asm commons-cli commons-codec commons-daemon apache-commons-io commons-lang commons-logging guava hawtjni-runtime jackson/jackson-core-asl jackson/jackson-mapper-asl jansi jansi-native tomcat-servlet-api jersey/jersey-core jersey/jersey-server jetty/jetty-continuation jetty/jetty-http jetty/jetty-io jetty/jetty-server jetty/jetty-util jline jsr-311 log4j netty protobuf slf4j/api xmlenc zookeeper
popd

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
  %{_bindir}/build-jar-repository -s . atinject aopalliance objectweb-asm/asm avro/avro apache-commons-io guava guice hamcrest/core jackson/jackson-core-asl jackson/jackson-mapper-asl jersey/jersey-core jersey/jersey-guice jersey/jersey-server jersey/jersey-servlet jsr-311 junit log4j netty paranamer/paranamer protobuf snappy-java
popd

pushd %{buildroot}/%{_datadir}/%{name}/yarn/lib
  %{__ln_s} %{_javadir}/%{name}/%{name}-annotations-%{hadoop_base_version}.jar .
  %{_bindir}/build-jar-repository -s . atinject aopalliance objectweb-asm/asm avro/avro cglib apache-commons-io guava guice hamcrest/core jackson/jackson-core-asl jackson/jackson-mapper-asl jersey/jersey-core jersey/jersey-guice jersey/jersey-server jersey/jersey-servlet jsr-311 junit log4j netty paranamer/paranamer protobuf snappy-java
popd

%if %{package_httpfs}
# httpfs
cp -arf $basedir/share/hadoop/httpfs/tomcat/bin/*.sh %{buildroot}/%{_libexecdir}/%{name}-httpfs
cp -arf $basedir/share/hadoop/httpfs/tomcat/bin/catalina-tasks.xml %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat/bin
cp -arf $basedir/share/hadoop/httpfs/tomcat/conf/* %{buildroot}/%{_sysconfdir}/%{name}/tomcat
cp -arf $basedir/share/hadoop/httpfs/tomcat/webapps %{buildroot}/%{_sharedstatedir}/%{name}-httpfs
pushd %{buildroot}/%{_datadir}/%{name}/httpfs/tomcat
  %{_bindir}/build-jar-repository -s bin tomcat/tomcat-juli commons-daemon
  %{__ln_s} %{_datadir}/tomcat/bin/bootstrap.jar bin
  for f in `ls %{buildroot}/%{_libexecdir}/%{name}-httpfs`
  do
    %{__ln_s} %{_libexecdir}/%{name}-httpfs/$f bin
  done
  %{__ln_s} %{_sysconfdir}/%{name}/tomcat conf 
  %{__ln_s} %{_javadir}/tomcat lib
  %{__ln_s} %{_var}/log/%{name}-httpfs logs
  %{__ln_s} %{_sharedstatedir}/%{name}-httpfs/webapps webapps
  %{__ln_s} %{_var}/cache/%{name}-httpfs/temp temp
  %{__ln_s} %{_var}/cache/%{name}-httpfs/work work
popd
%endif

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

# startup script customizations
cp -f %{SOURCE6} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop-datanode

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

%pre
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HDFS" --shell /sbin/nologin -M -r -g hdfs -G hadoop --home %{_var}/cache/%{name}-hdfs hdfs

%if %{package_httpfs}
%pre httpfs 
getent group httpfs >/dev/null || groupadd -r httpfs
getent passwd httpfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HTTPFS" --shell /sbin/nologin -M -r -g httpfs -G httpfs --home %{_var}/run/%{name}-httpfs httpfs
%endif

%pre yarn
getent group yarn >/dev/null || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Hadoop Yarn" --shell /sbin/nologin -M -r -g yarn -G hadoop --home %{_var}/cache/%{name}-yarn yarn

%pre mapreduce
getent group mapred >/dev/null || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Hadoop MapReduce" --shell /sbin/nologin -M -r -g mapred -G hadoop --home %{_var}/cache/%{name}-mapreduce mapred

%preun hdfs
%systemd_preun %{hdfs_services}

%preun mapreduce
%systemd_preun %{mapreduce_services}

%preun yarn
%systemd_preun %{yarn_services}

%if %{package_httpfs}
%preun httpfs
%systemd_preun %{httpfs_services}
%endif

%post hdfs
%systemd_post %{hdfs_services}

%post mapreduce
%systemd_post %{mapreduce_services}

%post yarn
%systemd_post %{yarn_services}

%if %{package_httpfs}
%post httpfs
%systemd_post %{httpfs_services}
%endif

%postun hdfs
%systemd_postun_with_restart %{hdfs_services}

%postun mapreduce
%systemd_postun_with_restart %{mapreduce_services}

%postun yarn
%systemd_postun_with_restart %{yarn_services}

%if %{package_httpfs}
%postun httpfs
%systemd_postun_with_restart %{httpfs_services}
%endif


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
%attr(0775,yarn,hadoop) %dir %{_var}/run/%{name}-yarn
%attr(0775,yarn,hadoop) %dir %{_var}/log/%{name}-yarn
%attr(1777,yarn,hadoop) %dir %{_var}/cache/%{name}-yarn

%files hdfs
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/hdfs/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/hdfs-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/hdfs.conf
%{_sysconfdir}/sysconfig/hadoop-datanode
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
%{_sbindir}/hdfs-config.sh
%{_sbindir}/update-hdfs-env.sh
%{_sbindir}/hadoop-setup-hdfs.sh
%{_tmpfilesdir}/hadoop-hdfs.conf
%attr(0775,hdfs,hadoop) %dir %{_var}/run/%{name}-hdfs
%attr(0775,hdfs,hadoop) %dir %{_var}/log/%{name}-hdfs
%attr(1777,hdfs,hadoop) %dir %{_var}/cache/%{name}-hdfs

%files mapreduce
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/mapreduce/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/mapred-env.sh
%config(noreplace) %{_sysconfdir}/%{name}/mapred-queues.xml
%config(noreplace) %{_sysconfdir}/%{name}/mapred-queues.xml.template
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml
%config(noreplace) %{_sysconfdir}/%{name}/mapred-site.xml.template
%config(noreplace) %{_sysconfdir}/security/limits.d/mapreduce.conf
%{_datadir}/%{name}/mapreduce
%{_javadir}/%{name}/%{name}-mapreduce*.jar
%{_javadir}/%{name}/%{name}-archives*.jar
%{_javadir}/%{name}/%{name}-datajoin*.jar
%{_javadir}/%{name}/%{name}-distcp*.jar
%{_javadir}/%{name}/%{name}-extras*.jar
%{_javadir}/%{name}/%{name}-gridmix*.jar
%{_javadir}/%{name}/%{name}-rumen*.jar
%{_javadir}/%{name}/%{name}-streaming*.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-mapreduce*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-archives*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-datajoin*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-distcp*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-extras*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-gridmix*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-rumen*.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-streaming*.pom
%{_mavendepmapfragdir}/%{name}-%{name}-mapreduce*
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
%attr(0775,mapred,hadoop) %dir %{_var}/run/%{name}-mapreduce
%attr(0775,mapred,hadoop) %dir %{_var}/log/%{name}-mapreduce
%attr(1777,mapred,hadoop) %dir %{_var}/cache/%{name}-mapreduce


%files
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
%attr(0775,httpfs,httpfs) %dir %{_var}/run/%{name}-httpfs
%attr(0775,httpfs,httpfs) %dir %{_var}/log/%{name}-httpfs
%endif

%files libhdfs
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/hdfs/*
%defattr(-,root,root)
%{_libdir}/libhdfs*
#%{_includedir}/hdfs.h
# -devel should be its own package
#%doc %{_docdir}/libhdfs-%{hadoop_version}

%files hdfs-fuse
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/hdfs/*
%defattr(-,root,root)
%{_bindir}/fuse_dfs
#%attr(0755,root,root) %{bin_hadoop}/hadoop-fuse-dfs

%files javadoc
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%doc %{_javadocdir}/%{name}
