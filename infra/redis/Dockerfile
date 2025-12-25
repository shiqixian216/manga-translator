FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/ubuntu:22.04

RUN apt-get update \
  && apt-get install -y redis-server \
  && rm -rf /var/lib/apt/lists/*

EXPOSE 6379
CMD ["redis-server", "--bind", "0.0.0.0", "--protected-mode", "no"]

