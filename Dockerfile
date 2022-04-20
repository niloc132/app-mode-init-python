ARG DH_VERS

FROM ghcr.io/deephaven/server:${DH_VERS}

ARG TF_VERS
ENV TF_VERS ${TF_VERS}

RUN pip install tensorflow==${TF_VERS}

