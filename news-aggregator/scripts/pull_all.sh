#!/bin/bash

git pull
ls | xargs -P10 -I{} git -C {} pull --recurse-submodules
ls | xargs -P10 -I{} git -C {} submodule foreach git pull origin main