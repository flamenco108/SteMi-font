#!/bin/bash

cat slnp-toomuch > sl-to
cat slnp-toolittle >> sl-to
./same-nry.py sl-to
