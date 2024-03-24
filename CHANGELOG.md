# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1] - 2023-10-18

### Added

- general: Add typing to variables
- general: Pydantic models and validations
- general: Pydantic settings
- maps_scrapper: FastAPI router for maps_scrapper
- maps_scrapper: Google Maps url generator
- maps_scrapper: Fake HTTP headers generator
- maps_scrapper: Method to remove duplicates
- maps_scrapper: Read company's name
- maps_scrapper: Read user's score
- maps_scrapper: Read user's number of reviews
- maps_scrapper: Read company's address
- maps_scrapper: Read company's phone number
- maps_scrapper: Read company's website
- aws_kinesis: Class to work with data_streams
- aws_kinesis: Class to work with data_analytics
- aws_kinesis: function to manage batch records for data streams

### Changed

- general: Refactor project to three layer architecture
- maps_scrapper: httpx client timeout set to 10s by default
