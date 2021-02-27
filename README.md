[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Build Status](https://travis-ci.org/fxbabin/expert_system.png)](https://travis-ci.org/42-AI/42ai_pdf_builder)

<p align="center">
  <img src="assets/logo-42-ai.png" width="200" alt="42 AI Logo" />
</p>

<h1 align="center">
	PDF Builder
</h1>
<h3 align="center">
	A PDF builder made to create all our subjects :rocket:
</h3>
<br/>

## One simple rule: Prefer pure markdown!

This pdf builder has an implicit rule. The more pure markdown your document is, the better it will look!

Concretely this means pure markdown syntax is better handled by this pdf builder than HTML one. 

This rule impacts:
- links (blue color)
- images (handle width, add a figure title)

You can find supported formats for lists, images, links, and table in the `assets/syntax_guidelines.md` file.

The pdf_builder supports two modes:
- simple (for a single project)
- bootcamp (for bootcamp days)

# Installation

## System installation

The pdf_builder uses latex and a library called pandoc, you can follow this [link](https://pandoc.org/installing.html) for the installation procedure of pandoc.

You can install the pdf_builder with pip

```console
pip install git+https://github.com/42-AI/42ai_pdf_builder.git
```

## Docker installation

The pdf builder can also use Docker to isolate the execution environment (like a virtual machine). We can install Docker using `assets/init_docker.sh` script.
This script was originally written by [Alexandre GV.](https://github.com/alexandregv/42toolbox), a 42 student.

A `Dockerfile` is available in the `assets` directory. 

### Container deployment

First, we need to build the docker image for pdf_builder. Our image will be named `pdf_builder`.

```console
cd assets/
DOCKER_BUILDKIT=1 docker build -t pdf_builder .
```

nb: the `DOCKER_BUILDKIT` option is an optimization for the build (parallelizes download and add a delta system for consecutive builds). It also has a cache you will need to prune if you want to save some space (see the end of README).

Then we can run the docker container. Our docker container will also be named `pdf_builder`. 

```console
docker run --name pdf_builder -d -t pdf_builder
```

### Pdf builds

First, we need to connect to the docker container.

```console
docker exec -it pdf_builder /bin/sh
```

We arrive in the `/data` directory of the container with the pdf_builder.

```console
$> ls
pdf_builder
$> cd pdf_builder
```

`pdf-builder simple` supports the following arguments :
- **project-title** : the project title
- **input-directory** : input directory
- **output-path** : Path to save the pdf to
- **logo-file** : Logo image file to use for the project
- **template-file** : Latex Template file to use for the project

`pdf-builder bootcamp` supports the following arguments :
- **bootcamp-title** : the bootcamp title
- **input-directory** : input directory
- **day-title** : Title of the day
- **output-path** : Path to save the pdf to
- **logo-file** : Logo image file to use for the project
- **template-file** : Latex Template file to use for the project

You can clone your project wherever you want and use the pdf_builder.

```console
git clone https://github.com/42-AI/bootcamp_data-engineering
```

Now, you can build your pdf.

```console
pdf-builder bootcamp -b "Data Engineering" -d /data/bootcamp_data-engineering/day00 -t "Day00 - PostgreSQL" -o day00.pdf
```

You now have a pdf file in your container. You can copy it out of your container with the following command.

```console
docker cp pdf_builder:/data/day00.pdf .
```

You finally have the pdf in your laptop filesystem, enjoy!

### Destroy Containers and Images

When you are done, you can destroy the container and image with the following commands.

```console
docker stop pdf_builder
docker rm pdf_builder
docker image rm pdf_builder
```

### Free caches and remaining images (DANGEROUS)

With this command, everything linked to docker (images, caches, containers) are removed. It's like if you restarted with a freshly installed docker. This allows you to free memory space.

```console
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker ps -a -q)
docker system prune -a