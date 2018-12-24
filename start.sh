#!/bin/bash
uwsgi --plugins=python3,http --http-socket :9090 --module server
