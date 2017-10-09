#!/usr/bin/env bash

[ -z "$HSPATH" ] || cd $HSPATH
python3 -m unittest
