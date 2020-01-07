#!/bin/sh

(cd "$(git rev-parse --show-toplevel)"; git subtree push --prefix api heroku master)
