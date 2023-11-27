# Dockerfiles

These describe how to build the docker images used by the project.

## Building

To build the docker images, run the following command from the **root** of the project:

`docker build --build-arg SETUPTOOLS_SCM_PRETEND_VERSION=v0.0.1000 -f dockerfiles/Dockerfile.user -t registry.atopile.io/atopile/atopile/user:latest .`

Again, you need to run this from the project root, not this directory.

NOTE: we take the "very high" version number of 1000 because we want to make our caches keep working
