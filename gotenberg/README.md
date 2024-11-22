# Gotenberg integration in Odoo


##Gotenberg is a Docker-powered stateless API for PDF files. 

**In other words:**

- It's a Docker image containing all the required dependencies; no need to install them on each environment.
- It scales smoothly and works nicely in a distributed context.
- It provides multipart/form-data endpoints for converting documents to PDF files, transforming them, merging them, and more!
- It has HTTP/2 support (H2C).

Gotenberg provides a developer-friendly API to interact with powerful tools like Chromium and LibreOffice 
to convert many documents (HTML, Markdown, Word, Excel, etc.) to PDF, transform them, merge them, and more!


## Quick Start

Open a terminal and run the following command:

```
docker run --rm -p 3000:3000 gotenberg/gotenberg:6
```

or

```
docker run --rm -p 3000:3000 thecodingmachine/gotenberg:6
```

The API is now available on your host at http://localhost:3000.

Head to the [documentation](https://gotenberg.dev/docs/about) to learn how to interact with it 🚀

## Configuration

For a service running in a docker, you need to add an environment variable **GOTENBERG_SERVER**

For a service running on a remote server, you need to specify the connection data in the settings.
## Use


## Development and Testing

### Requirements

There are a few things that we need for running the test suite.

- A database instance WITH demo data. So when you are creating a database from that database creation screen, make sure to mark to include demo data.
- Run odoo with the --test-enable flag
- Run odoo with the -d {my_database} flag
- Run odoo with the -i {modules_to_install} flag
- (optional) Sometimes it’s also nice to use --stop-after-init 

### Run The Tests
```shell
$ docker-compose stop
$ docker-compose run web \
    --test-enable \
    --stop-after-init \
    -d test_db \
    -i test_module
```