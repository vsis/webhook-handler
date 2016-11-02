FROM centos:7

MAINTAINER roddy <roddy.gonzalez.89@gmail.com>

RUN yum install -y epel-release; \
    yum install -y python-pip git; \
    git clone https://github.com/vsis/webhook-handler.git; \
    cd webhook-handler; \
    pip install -r requirements.txt; \
    yum clean all;

EXPOSE 5000

CMD ["python", "/webhook-handler/webhook-handler.py"]
