#!/bin/bash
/usr/bin/pip3 uninstall -y canvas-filter
poetry build
/usr/bin/pip3 install --user ./dist/canvas_filter-0.1.0-py3-none-any.whl
