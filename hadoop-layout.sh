HADOOP_PREFIX=/usr
HADOOP_COMMON_HOME=/usr
HADOOP_COMMON_DIR=share/hadoop/common
HADOOP_COMMON_LIB_JARS_DIR=share/hadoop/common/lib
HADOOP_COMMON_LIB_NATIVE_DIR=lib
HADOOP_CONF_DIR=/etc/hadoop
HADOOP_LIBEXEC_DIR=/usr/libexec

HADOOP_HDFS_HOME=$HADOOP_PREFIX
HDFS_DIR=share/hadoop/hdfs
HDFS_LIB_JARS_DIR=share/hadoop/hadoop/lib
HADOOP_PID_DIR=/var/run/hadoop-hdfs
HADOOP_LOG_DIR=/var/log/hadoop-hdfs
HADOOP_IDENT_STRING=hdfs

HADOOP_YARN_HOME=$HADOOP_PREFIX
YARN_DIR=share/hadoop/yarn
YARN_LIB_JARS_DIR=share/hadoop/yarn/lib
YARN_IDENT_STRING=yarn
YARN_PID_DIR=/var/run/hadoop-yarn
YARN_LOG_DIR=/var/log/hadoop-yarn
YARN_CONF_DIR=$HADOOP_CONF_DIR
YARN_IDENT_STRING=yarn

HADOOP_MAPRED_HOME=$HADOOP_PREFIX
MAPRED_DIR=share/hadoop/mapreduce
MAPRED_LIB_JARS_DIR=share/hadoop/mapreduce/lib
HADOOP_MAPRED_PID_DIR=/var/run/hadoop-mapreduce
HADOOP_MAPRED_LOG_DIR=/var/log/hadoop-mapreduce
HADOOP_MAPRED_IDENT_STRING=mapred

HTTPFS_CONFIG=/etc/hadoop
HTTPFS_LOG=/var/log/hadoop-httpfs
HTTPFS_TEMP=/var/run/hadoop-httpfs
HTTPFS_CATALINA_HOME=/usr
CATALINA_PID=/var/run/hadoop-httpfs/hadoop-$SVC_USER-httpfs.pid
CATALINA_BASE=/usr/share/hadoop/httpfs
CATALINA_TMPDIR=/var/run/hadoop-httpfs
# HTTPFS_HTTP_PORT
# HTTPFS_ADMIN_PORT
