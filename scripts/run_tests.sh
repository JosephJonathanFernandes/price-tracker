#!/bin/bash
# Run all tests with coverage
coverage run -m unittest discover tests
coverage report -m
