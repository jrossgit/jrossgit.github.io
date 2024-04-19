# James Ross's Blog

## Development Quickstart

This blog is constructed using [Jekyll](https://jekyllrb.com). More details about operating
Jekyll sites is available in their docs.

### Prerequisites

- Ruby 2.5.0 or higher
- RubyGems
- GCC and Make

Start serving to your local machine with the following commands:

```bash
bundle update
bundle install
bundle exec jekyll serve
```

Serve the site from an nginx container

```
docker run ...
```