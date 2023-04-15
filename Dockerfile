FROM python:3.9.16-alpine

RUN python -m pip install --upgrade pip \
    && python -m pip install 'flit>=3.8.0'

ENV FLIT_ROOT_INSTALL=1

COPY pyproject.toml .
RUN touch README.md \
    && mkdir -p src/osintbuddy \
    && python -m flit install --only-deps --deps develop \
    && rm -r pyproject.toml README.md src
