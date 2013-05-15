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

#
# Hadoop Fedora/RHEL RPM spec file
#

%define hadoop_base_version 2.0.2-alpha

Name:   hadoop
Version: 2.0.2
Release: 0.1%{?dist}
Summary: Hadoop is a software platform for processing vast amounts of data
License: Apache License v2.0
URL:    http://hadoop.apache.org/core/
Group:  Development/Libraries
Source0: %{name}-%{hadoop_base_version}.tar.gz
Source1: hadoop-layout.sh
Source2: hadoop.init
Source3: hadoop.sysconfig
Source4: hadoop-fuse.sysconfig
Source5: hadoop-hdfs.sysconfig
Source6: hadoop-httpfs.sysconfig
Source7: hadoop-mapreduce.sysconfig
Source8: hadoop-yarn.sysconfig
Source9: hadoop-datanode.sysconfig
Source10: hadoop-limits.conf
Source11: hadoop-core-site.xml
Source12: hadoop-hdfs-site.xml
Source13: hadoop-mapred-site.xml
Source14: hadoop-yarn-site.xml
Patch0: hadoop-fedora-integration.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -u -n)
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
Requires: zookeeper >= 3.4.0
Requires: psmisc
Requires: nc6
Requires: jetty
Requires: jersey
Requires: snappy-java

#%define hadoop_name hadoop
#%define etc_hadoop /etc/%{name}
#%define etc_yarn /etc/yarn
#%define etc_httpfs /etc/%{name}-httpfs
#%define config_hadoop %{etc_hadoop}/conf
#%define config_yarn %{etc_yarn}/conf
#%define config_httpfs %{etc_httpfs}/conf
#%define lib_hadoop_dirname /usr/lib
#%define lib_hadoop %{lib_hadoop_dirname}/%{name}
#%define lib_httpfs %{lib_hadoop_dirname}/%{name}-httpfs
#%define lib_hdfs %{lib_hadoop_dirname}/%{name}-hdfs
#%define lib_yarn %{lib_hadoop_dirname}/%{name}-yarn
#%define lib_mapreduce %{lib_hadoop_dirname}/%{name}-mapreduce
#%define log_hadoop_dirname /var/log
#%define log_hadoop %{log_hadoop_dirname}/%{name}
#%define log_yarn %{log_hadoop_dirname}/%{name}-yarn
#%define log_hdfs %{log_hadoop_dirname}/%{name}-hdfs
#%define log_httpfs %{log_hadoop_dirname}/%{name}-httpfs
#%define log_mapreduce %{log_hadoop_dirname}/%{name}-mapreduce
#%define run_hadoop_dirname /var/run
#%define run_hadoop %{run_hadoop_dirname}/hadoop
#%define run_yarn %{run_hadoop_dirname}/%{name}-yarn
#%define run_hdfs %{run_hadoop_dirname}/%{name}-hdfs
#%define run_httpfs %{run_hadoop_dirname}/%{name}-httpfs
#%define run_mapreduce %{run_hadoop_dirname}/%{name}-mapreduce
#%define state_hadoop_dirname /var/lib
#%define state_hadoop %{state_hadoop_dirname}/hadoop
#%define state_yarn %{state_hadoop_dirname}/%{name}-yarn
#%define state_hdfs %{state_hadoop_dirname}/%{name}-hdfs
#%define state_mapreduce %{state_hadoop_dirname}/%{name}-mapreduce
#%define bin_hadoop %{_bindir}
#%define man_hadoop %{_mandir}
#%define doc_hadoop %{_docdir}/%{name}-%{hadoop_version}
#%define httpfs_services httpfs
#%define mapreduce_services mapreduce-historyserver
#%define hdfs_services hdfs-namenode hdfs-secondarynamenode hdfs-datanode hdfs-zkfc
#%define yarn_services yarn-resourcemanager yarn-nodemanager yarn-proxyserver
#%define hadoop_services %{hdfs_services} %{mapreduce_services} %{yarn_services} %{httpfs_services}
## Hadoop outputs built binaries into %{hadoop_build}
#%define hadoop_build_path build
#%define static_images_dir src/webapps/static/images

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

%description hdfs
Hadoop Distributed File System (HDFS) is the primary storage system used by 
Hadoop applications. HDFS creates multiple replicas of data blocks and distributes 
them on compute nodes throughout a cluster to enable reliable, extremely rapid 
computations.

%package yarn
Summary: The Hadoop NextGen MapReduce (YARN)
Group: System/Daemons
Requires: %{name} = %{version}-%{release}

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

%description mapreduce
Hadoop MapReduce is a programming model and software framework for writing
applications that rapidly process vast amounts of data in parallel on large
clusters of compute nodes.


#%package hdfs-namenode
#Summary: The Hadoop namenode manages the block locations of HDFS files
#Group: System/Daemons
#Requires: %{name}-hdfs = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}
#
#%description hdfs-namenode
#The Hadoop Distributed Filesystem (HDFS) requires one unique server, the
#namenode, which manages the block locations of files on the filesystem.
#
#
#%package hdfs-secondarynamenode
#Summary: Hadoop Secondary namenode
#Group: System/Daemons
#Requires: %{name}-hdfs = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}
#
#%description hdfs-secondarynamenode
#The Secondary Name Node periodically compacts the Name Node EditLog
#into a checkpoint.  This compaction ensures that Name Node restarts
#do not incur unnecessary downtime.
#
#%package hdfs-zkfc
#Summary: Hadoop HDFS failover controller
#Group: System/Daemons
#Requires: %{name}-hdfs = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}
#
#%description hdfs-zkfc
#The Hadoop HDFS failover controller is a ZooKeeper client which also
#monitors and manages the state of the NameNode. Each of the machines
#which runs a NameNode also runs a ZKFC, and that ZKFC is responsible
#for: Health monitoring, ZooKeeper session management, ZooKeeper-based
#election.
#
#%package hdfs-datanode
#Summary: Hadoop Data Node
#Group: System/Daemons
#Requires: %{name}-hdfs = %{version}-%{release}
#Requires: apache-commons-daemon-jsvc
#Requires(pre): %{name} = %{version}-%{release}
#
#%description hdfs-datanode
#The Data Nodes in the Hadoop Cluster are responsible for serving up
#blocks of data over the network to Hadoop Distributed Filesystem
#(HDFS) clients.

%package httpfs
Summary: HTTPFS for Hadoop
Group: System/Daemons
Requires: %{name}-hdfs = %{version}-%{release}, bigtop-tomcat
Requires(pre): %{name} = %{version}-%{release}

%description httpfs
The server providing HTTP REST API support for the complete
FileSystem/FileContext interface in HDFS.

#%package yarn-resourcemanager
#Summary: YARN Resource Manager
#Group: System/Daemons
#Requires: %{name}-yarn = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}
#
#%description yarn-resourcemanager
#The resource manager manages the global assignment of compute resources to
#applications
#
#%package yarn-nodemanager
#Summary: YARN Node Manager
#Group: System/Daemons
#Requires: %{name}-yarn = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}
#
#%description yarn-nodemanager
#The NodeManager is the per-machine framework agent who is responsible for
#containers, monitoring their resource usage (cpu, memory, disk, network) and
#reporting the same to the ResourceManager/Scheduler.
#
#%package yarn-proxyserver
#Summary: YARN Web Proxy
#Group: System/Daemons
#Requires: %{name}-yarn = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}
#
#%description yarn-proxyserver
#The web proxy server sits in front of the YARN application master web UI.
#
#%package mapreduce-historyserver
#Summary: MapReduce History Server
#Group: System/Daemons
#Requires: %{name}-mapreduce = %{version}-%{release}
#Requires(pre): %{name} = %{version}-%{release}
#
#%description mapreduce-historyserver
#The History server keeps records of the different activities being performed
#on an Apache Hadoop cluster

%package client
Summary: Hadoop client side dependencies
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}

%description client
Installation of this package will provide you with all the dependencies for
Apache Hadoop clients.

#%package conf-pseudo
#Summary: Pseudo-distributed Hadoop configuration
#Group: System/Daemons
#Requires: %{name} = %{version}-%{release}
#Requires: %{name}-hdfs-namenode = %{version}-%{release}
#Requires: %{name}-hdfs-datanode = %{version}-%{release}
#Requires: %{name}-hdfs-secondarynamenode = %{version}-%{release}
#Requires: %{name}-yarn-resourcemanager = %{version}-%{release}
#Requires: %{name}-yarn-nodemanager = %{version}-%{release}
#Requires: %{name}-mapreduce-historyserver = %{version}-%{release}
#
#%description conf-pseudo
#Contains configuration files for a "pseudo-distributed" Hadoop deployment.
#In this mode, each of the hadoop components runs as a separate Java process,
#but all on the same machine.
#
#%package doc
#Summary: Hadoop Documentation
#Group: Documentation
#%description doc
#Documentation for Hadoop

%package libhdfs
Summary: Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name}-hdfs = %{version}-%{release}
# TODO: reconcile libjvm

%description libhdfs
Hadoop Filesystem Library

%package hdfs-fuse
Summary: Mountable HDFS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libhdfs = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: fuse

%description hdfs-fuse
These projects (enumerated below) allow HDFS to be mounted (on most flavors of
Unix) as a standard file system using

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

#%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin hadoop-hdfs-project/hadoop-hdfs-httpfs
#%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin hadoop-mapreduce-project
#%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin hadoop-project-dist
#%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin hadoop-project
#%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin hadoop-tools/hadoop-rumen
#%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin hadoop-tools/hadoop-streaming
#%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin hadoop-yarn-project

%build
mvn-rpmbuild -Drequire.snappy=true -Pdist,native -DskipTests package javadoc:aggregate

%check
mvn-rpmbuild -Pnative test -Dmaven.test.failure.ignore=true

%clean
rm -rf %{buildroot}

#########################
#### INSTALL SECTION ####
#########################
%install
install -d -m 0755 %{buildroot}/%{_libdir}
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/hadoop-hdfs
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/hadoop-httpfs/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/hadoop-hdfs
install -d -m 0755 %{buildroot}/%{_datadir}/hadoop-httpfs
install -d -m 0755 %{buildroot}/%{_javadir}
install -d -m 0755 %{buildroot}/%{_javadocdir}/%{name}
install -d -m 0755 %{buildroot}/%{_sysconfdir}/sysconfig
install -d -m 0755 %{buildroot}/%{_sysconfdir}/hadoop/tomcat

basedir='hadoop-dist/target/hadoop-%{hadoop_base_version}'

for dir in bin libexec sbin
do
  cp -arf $basedir/$dir %{buildroot}/%{_prefix}
done

# We don't care about this binary
rm -f %{buildroot}/%{_bindir}/test-container-executor

cp -arf $basedir/etc %{buildroot}

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
  target="hadoop-$dir"
  install -d -m 0755 %{buildroot}/%{_javadir}/$target
  find $basedir/share/hadoop/$dir -name *-%{hadoop_base_version}.jar | xargs cp -af -t %{buildroot}/%{_javadir}/$target
done
mv -f %{buildroot}/%{_javadir}/hadoop-tools/* %{buildroot}/%{_javadir}/hadoop-mapreduce
# TODO
#rm -rf %{buildroot}/%{_javadir}/hadoop-tools

# httpfs
cp -arf $basedir/share/hadoop/httpfs/tomcat/conf/* %{buildroot}/%{_sysconfdir}/hadoop/tomcat
cp -arf $basedir/share/hadoop/httpfs/tomcat/webapps %{buildroot}/%{_sharedstatedir}/hadoop-httpfs
ln -s %{_sysconfdir}/hadoop/tomcat %{buildroot}/%{_datadir}/hadoop-httpfs/conf 
ln -s %{_javadir}/tomcat %{buildroot}/%{_datadir}/hadoop-httpfs/lib
ln -s %{_var}/log/hadoop-httpfs %{buildroot}/%{_datadir}/hadoop-httpfs/logs
ln -s %{_sharedstatedir}/hadoop-httpfs/webapps %{buildroot}/%{_datadir}/hadoop-httpfs/webapps
# TODO
#rm -rf %{buildroot}/%{_datadir}/hadoop-httpfs/lib

# install hdfs webapp bits
cp -arf $basedir/share/hadoop/hdfs/webapps %{buildroot}/%{_datadir}/hadoop-hdfs

# javadocs
cp -arf target/site/apidocs/* %{buildroot}/%{_javadocdir}/%{name}

# hadoop layout. Convert to appropriate lib location for 32 and 64 bit archs
lib=$(echo %{?_libdir} | sed -e 's:/usr/\(.*\):\1:')
if [ "$lib" = "%_libdir" ]; then
  echo "_libdir is not located in /usr.  Lib location is wrong"
  exit 1
fi
sed -e "s|^HADOOP_COMMON_LIB_NATIVE_DIR\s*=.*|HADOOP_COMMON_LIB_NATIVE_DIR=$lib|" %{SOURCE1} > %{buildroot}/%{_libexecdir}/hadoop-layout.sh

# default locations
cp -f %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop
cp -f %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop-fuse
cp -f %{SOURCE5} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop-hdfs
cp -f %{SOURCE6} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop-httpfs
cp -f %{SOURCE7} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop-mapreduce
cp -f %{SOURCE8} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop-yarn
cp -f %{SOURCE9} %{buildroot}/%{_sysconfdir}/sysconfig/hadoop-datanode

# default config
cp -f %{SOURCE11} %{buildroot}/%{_sysconfdir}/hadoop/core-site.xml
cp -f %{SOURCE12} %{buildroot}/%{_sysconfdir}/hadoop/hdfs-site.xml
cp -f %{SOURCE13} %{buildroot}/%{_sysconfdir}/hadoop/mapred-site.xml
cp -f %{SOURCE14} %{buildroot}/%{_sysconfdir}/hadoop/yarn-site.xml

#bash %{SOURCE2} \
#  --distro-dir=$RPM_SOURCE_DIR \
#  --build-dir=$PWD/build \
#  --httpfs-dir=$RPM_BUILD_ROOT%{lib_httpfs} \
#  --system-include-dir=$RPM_BUILD_ROOT%{_includedir} \
#  --system-lib-dir=$RPM_BUILD_ROOT%{_libdir} \
#  --system-libexec-dir=$RPM_BUILD_ROOT/%{lib_hadoop}/libexec \
#  --hadoop-etc-dir=$RPM_BUILD_ROOT%{etc_hadoop} \
#  --httpfs-etc-dir=$RPM_BUILD_ROOT%{etc_httpfs} \
#  --prefix=$RPM_BUILD_ROOT \
#  --doc-dir=$RPM_BUILD_ROOT%{doc_hadoop} \
#  --example-dir=$RPM_BUILD_ROOT%{doc_hadoop}/examples \
#  --native-build-string=%{hadoop_arch} \
#  --installed-lib-dir=%{lib_hadoop} \
#  --man-dir=$RPM_BUILD_ROOT%{man_hadoop} \

install -d -m 0755 %{buildroot}/%{_initddir}/

# init scripts
for service in hdfs-namenode hdfs-datanode hdfs-secondarynamenode hdfs-zkfc mapreduce-historyserver yarn-nodemanager yarn-proxyserver yarn-resourcemanager
do
  d=`echo -n $service | cut -d'-' -f 2 | sed -e 's/^./\U&/g'`
  sed -e "s|DESC|Hadoop $d|g" %{SOURCE2} > %{buildroot}/%{_initddir}/hadoop-$service
  sed -i "s|\$daemon|$service|g" %{buildroot}/%{_initddir}/hadoop-$service
done

# httpfs is special of course
sed -e "s|DESC|Hadoop Httpfs|g" %{SOURCE2} > %{buildroot}/%{_initddir}/hadoop-httpfs
sed -i "s|\$daemon|httpfs|g" %{buildroot}/%{_initddir}/hadoop-httpfs

#
## Install top level /etc/default files
#install -d -m 0755 $RPM_BUILD_ROOT/etc/default
#cp $RPM_SOURCE_DIR/hadoop.default $RPM_BUILD_ROOT/etc/default/hadoop
## FIXME: BIGTOP-463
#echo 'export JSVC_HOME=%{libexecdir}/bigtop-utils' >> $RPM_BUILD_ROOT/etc/default/hadoop
#%__cp $RPM_SOURCE_DIR/%{name}-fuse.default $RPM_BUILD_ROOT/etc/default/%{name}-fuse
#
## Generate the init.d scripts
#for service in %{hadoop_services}
#do
#       init_file=$RPM_BUILD_ROOT/%{_initddir}/%{name}-${service}
#       # On RedHat, SuSE and Mageia run-level 2 is networkless, hence excluding it
#       env CHKCONFIG="345 85 15"       \
#           INIT_DEFAULT_START="3 4 5"  \
#           INIT_DEFAULT_STOP="0 1 2 6" \
#         bash $RPM_SOURCE_DIR/init.d.tmpl $RPM_SOURCE_DIR/%{name}-${service}.svc > $init_file
#       chmod 755 $init_file
#       cp $RPM_SOURCE_DIR/${service/-*/}.default $RPM_BUILD_ROOT/etc/default/%{name}-${service}
#       chmod 644 $RPM_BUILD_ROOT/etc/default/%{name}-${service}
#done
#
# Install security limits
install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/security/limits.d
for limit in hdfs yarn mapreduce
do
  sed -e "s|name|${limit:0:6}|" %{SOURCE10} > %{buildroot}/%{_sysconfdir}/security/limits.d/${limit}.conf
done
#install -m 0644 %{SOURCE8} $RPM_BUILD_ROOT/etc/security/limits.d/hdfs.conf
#install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT/etc/security/limits.d/yarn.conf
#install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT/etc/security/limits.d/mapreduce.conf
#
## Install fuse default file
#%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
#%__cp %{SOURCE4} $RPM_BUILD_ROOT/etc/default/hadoop-fuse
#
# /var/lib/*/cache
install -d -m 1777 $RPM_BUILD_ROOT/%{_sharedstatedir}/hadoop-yarn/cache
install -d -m 1777 $RPM_BUILD_ROOT/%{_sharedstatedir}/hadoop-hdfs/cache
install -d -m 1777 $RPM_BUILD_ROOT/%{_sharedstatedir}/hadoop-mapreduce/cache
# /var/log/*
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/log/hadoop-yarn
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/log/hadoop-hdfs
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/log/hadoop-mapreduce
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/log/hadoop-httpfs
# /var/run/*
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/run/hadoop-yarn
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/run/hadoop-hdfs
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/run/hadoop-mapreduce
install -d -m 0775 $RPM_BUILD_ROOT/%{_var}/run/hadoop-httpfs

%pre
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null   || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HDFS" --shell /bin/bash -M -r -g hdfs -G hadoop --home %{state_hdfs} hdfs

%pre httpfs 
getent group httpfs >/dev/null   || groupadd -r httpfs
getent passwd httpfs >/dev/null || /usr/sbin/useradd --comment "Hadoop HTTPFS" --shell /bin/bash -M -r -g httpfs -G httpfs --home %{run_httpfs} httpfs

%pre yarn
getent group yarn >/dev/null   || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Hadoop Yarn" --shell /bin/bash -M -r -g yarn -G hadoop --home %{state_yarn} yarn

%pre mapreduce
getent group mapred >/dev/null   || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Hadoop MapReduce" --shell /bin/bash -M -r -g mapred -G hadoop --home %{state_mapreduce} mapred

#%post
#%{alternatives_cmd} --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.empty 10
#
#%post httpfs
#%{alternatives_cmd} --install %{config_httpfs} %{name}-httpfs-conf %{etc_httpfs}/conf.empty 10
#chkconfig --add %{name}-httpfs

%preun
if [ "$1" = 0 ]; then
  # Stop any services that might be running
  for service in %{hadoop_services}
  do
     service hadoop-$service stop 1>/dev/null 2>/dev/null || :
  done
#  %{alternatives_cmd} --remove %{name}-conf %{etc_hadoop}/conf.empty || :
fi

%preun httpfs
if [ $1 = 0 ]; then
  service %{name}-httpfs stop > /dev/null 2>&1
  chkconfig --del %{name}-httpfs
#  %{alternatives_cmd} --remove %{name}-httpfs-conf %{etc_httpfs}/conf.empty || :
fi

%postun httpfs
if [ $1 -ge 1 ]; then
  service %{name}-httpfs condrestart >/dev/null 2>&1
fi


%files yarn
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/yarn/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/hadoop/yarn-env.sh
%config(noreplace) %{_sysconfdir}/hadoop/yarn-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/yarn.conf
%{_sysconfdir}/sysconfig/hadoop-yarn
%{_initddir}/%{name}-yarn-nodemanager
%{_initddir}/%{name}-yarn-proxyserver
%{_initddir}/%{name}-yarn-resourcemanager
%{_libexecdir}/yarn-config.sh
%{_javadir}/hadoop-yarn
%attr(6050,root,yarn) %{_bindir}/container-executor
%{_bindir}/yarn
%{_sbindir}/yarn-daemon.sh
%{_sbindir}/yarn-daemons.sh
%{_sbindir}/start-yarn.sh
%{_sbindir}/stop-yarn.sh
%attr(0775,yarn,hadoop) %dir %{_var}/run/hadoop-yarn
%attr(0775,yarn,hadoop) %dir %{_var}/log/hadoop-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/lib/hadoop-yarn
%attr(1777,yarn,hadoop) %dir %{_var}/lib/hadoop-yarn/cache

%files hdfs
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/hdfs/*
%defattr(-,root,root)
#%config(noreplace) /etc/default/hadoop-fuse
%config(noreplace) %{_sysconfdir}/hadoop/hdfs-site.xml
%config(noreplace) %{_sysconfdir}/security/limits.d/hdfs.conf
%{_sysconfdir}/sysconfig/hadoop-datanode
%{_sysconfdir}/sysconfig/hadoop-hdfs
%{_javadir}/hadoop-hdfs
%{_datadir}/hadoop-hdfs
%{_initddir}/%{name}-hdfs-datanode
%{_initddir}/%{name}-hdfs-namenode
%{_initddir}/%{name}-hdfs-secondarynamenode
%{_initddir}/%{name}-hdfs-zkfc
%{_libexecdir}/hdfs-config.sh
%{_bindir}/hdfs
%{_sbindir}/distribute-exclude.sh
%{_sbindir}/refresh-namenodes.sh
%{_sbindir}/hdfs-config.sh
%{_sbindir}/update-hdfs-env.sh
%{_sbindir}/hadoop-setup-hdfs.sh
%attr(0775,hdfs,hadoop) %dir %{_var}/run/hadoop-hdfs
%attr(0775,hdfs,hadoop) %dir %{_var}/log/hadoop-hdfs
%attr(0755,hdfs,hadoop) %dir %{_sharedstatedir}/hadoop-hdfs
%attr(1777,hdfs,hadoop) %dir %{_sharedstatedir}/hadoop-hdfs/cache

%files mapreduce
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/mapreduce/*
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/hadoop/mapred-site.xml
%config(noreplace) %{_sysconfdir}/hadoop/mapred-env.sh
%config(noreplace) %{_sysconfdir}/security/limits.d/mapreduce.conf
%{_sysconfdir}/sysconfig/hadoop-mapreduce
%{_javadir}/hadoop-mapreduce
%{_libexecdir}/mapred-config.sh
%{_initddir}/%{name}-mapreduce-historyserver
# TODO: Fix MAPREDUCE-3980 issue
%{_bindir}/mapred
%{_sbindir}/mr-jobhistory-daemon.sh
%attr(0775,mapred,hadoop) %dir %{_var}/run/hadoop-mapreduce
%attr(0775,mapred,hadoop) %dir %{_var}/log/hadoop-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/lib/hadoop-mapreduce
%attr(1777,mapred,hadoop) %dir %{_var}/lib/hadoop-mapreduce/cache


%files
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%defattr(-,root,root)
#%config(noreplace) %{_sysconfdir}/hadoop/core-site.xml
#%config(noreplace) %{_sysconfdir}/hadoop/hadoop-metrics.properties
#%config(noreplace) %{_sysconfdir}/hadoop/hadoop-metrics2.properties
#%config(noreplace) %{_sysconfdir}/hadoop/log4j.properties
#%config(noreplace) %{_sysconfdir}/hadoop/slaves
#%config(noreplace) %{_sysconfdir}/hadoop/ssl-client.xml.example
#%config(noreplace) %{_sysconfdir}/hadoop/ssl-server.xml.example
%config(noreplace) %{_sysconfdir}/hadoop/hadoop-env.sh
%{_sysconfdir}/sysconfig/hadoop
%{_javadir}/hadoop-common
%config(noreplace) %{_sysconfdir}/hadoop
%{_libexecdir}/hadoop-config.sh
%{_libexecdir}/hadoop-layout.sh
%{_bindir}/hadoop
%{_bindir}/rcc
%{_bindir}/fuse_dfs
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
#%{man_hadoop}/man1/hadoop.1.*

#%files doc
#%defattr(-,root,root)
#%doc %{doc_hadoop}

%files httpfs
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%defattr(-,root,root)
#%config(noreplace) %{etc_httpfs}/conf.empty
#%config(noreplace) /etc/default/%{name}-httpfs
%config(noreplace) %{_sysconfdir}/hadoop/httpfs-env.sh
%config(noreplace) %{_sysconfdir}/hadoop/tomcat
%{_sysconfdir}/sysconfig/hadoop-httpfs
%{_libexecdir}/httpfs-config.sh
%{_initddir}/%{name}-httpfs
%{_sbindir}/httpfs.sh
%{_datadir}/hadoop-httpfs
%{_sharedstatedir}/hadoop-httpfs
%attr(0775,httpfs,httpfs) %dir %{_var}/run/hadoop-httpfs
%attr(0775,httpfs,httpfs) %dir %{_var}/log/hadoop-httpfs

# Service file management RPMs
#%define service_macro() \
#%files %1 \
#%defattr(-,root,root) \
#%{_initddir}/%{name}-%1 \
#%config(noreplace) /etc/default/%{name}-%1 \
#%post %1 \
#chkconfig --add %{name}-%1 \
#\
#%preun %1 \
#if [ $1 = 0 ]; then \
#  service %{name}-%1 stop > /dev/null 2>&1 \
#  chkconfig --del %{name}-%1 \
#fi \
#%postun %1 \
#if [ $1 -ge 1 ]; then \
#  service %{name}-%1 condrestart >/dev/null 2>&1 \
#fi

#%service_macro hdfs-namenode
#%service_macro hdfs-secondarynamenode
#%service_macro hdfs-zkfc
#%service_macro hdfs-datanode
#%service_macro yarn-resourcemanager
#%service_macro yarn-nodemanager
#%service_macro yarn-proxyserver
#%service_macro mapreduce-historyserver

# Pseudo-distributed Hadoop installation
#%post conf-pseudo
#%{alternatives_cmd} --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.pseudo 30
#
#%preun conf-pseudo
#if [ "$1" = 0 ]; then
#        %{alternatives_cmd} --remove %{name}-conf %{etc_hadoop}/conf.pseudo
#        rm -f %{etc_hadoop}/conf
#fi
#
#%files conf-pseudo
#%defattr(-,root,root)
#%config(noreplace) %attr(755,root,root) %{etc_hadoop}/conf.pseudo

# TODO
%files client
%defattr(-,root,root)
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
#%{lib_hadoop}/client

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
#%attr(0644,root,root) %config(noreplace) /etc/default/hadoop-fuse
%{_sysconfdir}/sysconfig/hadoop-fuse
%attr(0755,root,root) %{_bindir}/fuse_dfs
#%attr(0755,root,root) %{bin_hadoop}/hadoop-fuse-dfs

%files javadoc
%doc hadoop-dist/target/hadoop-%{hadoop_base_version}/share/doc/hadoop/common/*
%doc %{_javadocdir}/%{name}
