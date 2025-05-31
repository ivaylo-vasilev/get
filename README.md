# Get - files downloader
Download files from Internet.
---

**Get** is a CLI program with a main purpose to download files from the Internet. Written in *Python*, **Get** uses the **requests** library to perform the HTTP operations. The very first version was able only to download files and show HEADERS information using the optional argument `-i`. Over the time I added more options to the program. You can see them by typing the `--help`:

```

usage: get [-h] [-o <file>] [-d <directory>] [-c] [-i] [-p] [--status] [--user-agent <string>]
           [--version]
           [URL]

Get - files downloader

positional arguments:
  URL                   specify URL

options:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        specify file name
  -d <directory>, --directory <directory>
                        specify download directory
  -c, --check           check file size
  -i, --info            show headers
  -p, --print           show response in terminal window
  --status              show http status code
  --user-agent <string>
                        set user-agent
  --version             show program version

(c)2025 Ivaylo Vasilev

```
