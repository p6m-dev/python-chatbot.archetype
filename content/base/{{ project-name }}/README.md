# {{ project-prefix }}-{{ app-name }} Ai Agent

## Project Initialization

Prior to performing any action on this project, you must first initialize it.  This ensures:

* Dependencies are Installed
* A Virtual Environment is Created
* Project Management Commands are Installed

Having your project property initialized ensures that the project will smoothly load into your IDE, Run, Build, and Package.

```shell
poetry install
```

## Local Development 

Regardless of your project type, you can run and test your project using common conventions. 

Running:
```shell
poetry run main
```

Testing:
```shell
poetry run pytest
````

## Containerization

Poetry commands have been set up to build and run your project in a containerized environment with a consistent interface.

Building:
```shell
poetry run docker-build
```

Running:
```shell
poetry run docker-run
```