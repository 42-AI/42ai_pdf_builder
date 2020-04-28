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

# Installation

## Docker

The pdf builder uses Docker to isolate the execution environment (like a virtual machine). We can install Docker using `assets/init_docker.sh` script.
This script was originally written by [Alexandre GV.](https://github.com/alexandregv/42toolbox), a student at 42.

## Container deployment

First, we need to build the docker image for pdf_builder. Our image will be named `pdf_builder`.

```console
DOCKER_BUILDKIT=1 docker build -t pdf_builder .
```

nb: the `DOCKER_BUILDKIT` option is an optimization for the build (parallelizes download and add a delta system for consecutive builds). It also has a cache you need to prune if you want to save some space (see the end of README).

Then we can run the docker container. Our docker container will also be named `pdf_builder`. 

```console
docker run --name pdf_builder -d -t pdf_builder
```

The container is ready for use!

## Pdf builds

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

Here we find the python project `pdf_builder`. Like a script, it can take the following arguments :
- **bootcamp_title** : the bootcamp title (required) -> "Data Engineering"
- **pdf_title** : title of the pdf (required) -> "Day00 - PostgreSQL")
- **output_file** : name of the pdf output file (required) -> "day00.pdf"
- **input_dir** : the input directory for the day (conflicts with input_file option) -> "bootcamp_data_engineering/day00/"
- **input_file** : the input file name (for documentation purpose) -> "bootcamp_data_engineering/day00/psycopg2_documentation.md"

The program arguments can also be found with the following command.

```console
python3 pdf_builder --help
```

Once you are in the pdf_builder directory, you can clone your project.

```console
git clone https://github.com/42-AI/bootcamp_data-engineering
```

Now, you can build your pdf.

```console
python3 pdf_builder -b "Data Engineering" -d ~/bootcamp_data-engineering/day00 -t "Day00 - PostgreSQL" -o day00.pdf
```

You now have a pdf file in your container. You can copy it out of your container with the following command.

```console
docker cp pdf_builder:/data/day00.pdf .
```

You finally have the pdf in your laptop filesystem, enjoy!

## Destroy Containers and Images

When you are done, you can destroy the container and image with the following commands.

```console
docker stop pdf_builder
docker rm pdf_builder
docker image rm pdf_builder
```

## Free caches and remaining images (DANGEROUS)

With this command, everything linked to docker (images, caches, containers) are removed. It's like if you restarted with a freshly installed docker. This allows you to free memory space.

```console
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker ps -a -q)
docker system prune -a
```

## Contributors

- Francois-Xavier Babin (fbabin@student.42.fr)
- Mathilde Boivin (mboivin@student.42.fr)
