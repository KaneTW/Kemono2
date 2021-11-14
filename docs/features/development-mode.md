# Development Mode

## Table of contents
- [General Description](#general-description)
- [Issues](#issues)

## General Description
Development mode provides a way to create a dev environment from scratch for ease of development and testing.

### Location
Development-only files live in their `development` folder, located in the root of a project, which exposes its own exported modules in its index file. Only exports declared within in are allowed to be imported outside and only do it conditionally by checking for the presence of development environment variable beforehand.
The folder structure follows the same logic as `src` folder, i.e. it can have its own `lib`, `endpoints`, `types` and even `internals` folders.
The server also provides `/development` endpoint, which allows to access various features.

### Features

#### Test entries
Generates test entries in the database. There are two mechanisms for generation:
- Seeded
- Random

Seeded generation outputs the same result each use and therefore should error out on the second use. The main usecase is to populate the initial test database.
Random generation allows to create new random entries regardless of circumstances. The main usecase is to add random entries of any table during development process.

## Issues

- Due to some underlying changes of importing process the test import doesn't work
