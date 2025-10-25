#!/usr/bin/env bash
set -e
apt-get update && apt-get install -y build-essential rustc cargo
pip install --upgrade pip
pip install -r requirements.txt
