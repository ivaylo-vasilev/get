import sys
import os
import argparse
import requests
from colorama import init, Fore

init(autoreset=True)

GRN = Fore.GREEN
YLW = Fore.YELLOW
RED = Fore.RED
RST = Fore.RESET

PROG = f"Get 2025.2.1 on {sys.platform} (c)Ivaylo Vasilev"
USER_AGENT = f"Get/2025.2.1-{sys.platform}"

parser = argparse.ArgumentParser(prog="get", description="Get - files downloader", epilog="(c)2025 Ivaylo Vasilev")
parser.add_argument("url", metavar="URL", nargs="?", help="specify URL")
parser.add_argument("-n", "--name", metavar="NAME", help="specify file name")
parser.add_argument("-d", "--directory", metavar="DIR", help="specify download directory")
parser.add_argument("-c", "--check", action="store_true", help="check file size")
parser.add_argument("-i", "--info", action="store_true", help="show headers")
parser.add_argument("-p", "--print", action="store_true", help="show response in terminal window")
parser.add_argument("--status", action="store_true", help="show http status code")
parser.add_argument("--user-agent", metavar="STR", default=USER_AGENT, help="set user-agent")
parser.add_argument("--version", action="version", version=PROG, help="show program version")
args = parser.parse_args()


http_codes = {
    200: "OK", 204: "No Content", 300: "Multiple Choices", 301: "Moved Permanently",
    400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found",
    408: "Request Timeout", 500: "Internal Server Error", 502: "Bad Gateway", 
    503: "Service Unavailable", 504: "Gateway Timeout"
}

mime_types = [
    "text/plain",
    "text/html",
    "application/json",
    "application/x-httpd-php"
]


def main():
    url = args.url
    if url == None:
        print(f"{RED}error:{RST} missing URL")
        parser.print_usage()
        sys.exit(1)
    
    banner()

    if args.user_agent != USER_AGENT:
        print(f"{GRN}[+]{RST} Using spoofed User-Agent")
        print("----------------------------")
    
    print(download(url))


def download(url):
    try:
        r = requests.get(url, headers={"User-Agent": args.user_agent}, stream=True)
        if args.status:
            http_code = r.status_code
            if http_code in http_codes:
                print(f"Status code: {http_code} [ {http_codes[http_code]} ]")
            else:
                print(f"Status code: {http_code} [ ... ]")
            sys.exit(0)
        if args.info:
            info(r)
            sys.exit(0)
        elif args.print:
            for mime_type in mime_types:
                try:
                    if mime_type in r.headers["Content-type"]:
                        content_size = sys.getsizeof(r.content)
                        if content_size <= 50000:
                            print("")
                            print(f"Status: {r.status_code}")
                            print("")
                            print(r.text)
                            sys.exit(0)
                        else:
                            print(f"{RED}Warning:{RST} Content length is too big to print in terminal")
                            sys.exit(5)
                except KeyError as e:
                    print(f"{RED}Error:{RST} Missing {e} in header")
                    sys.exit(3)
            print(f"{RED}Error:{RST} MIME type is not supported for print in terminal")
            sys.exit(6)
        status_code = r.status_code
        if status_code != 200:
            print(f"Status: {status_code} ... {RED}error{RST}")
            sys.exit(2)
        try:
            file_length = r.headers["Content-Length"]
            file_size = float(int(file_length) / 1024 / 1024)
        except KeyError as e:
            print(f"{RED}Error:{RST} Missing {e} in header")
            file_size = 0.00
        try:
            file_type = r.headers["Content-type"]
        except KeyError as e:
            print(f"{RED}Error:{RST} Missing {e} in header")
            file_type = "Unknown"

        if args.name:
            ext = url.split(".")[-1]
            filename = f"{args.name}.{ext}"
        else:
            filename = url.split("/")[-1]
        
        if args.check:
            if file_size == 0.00:
                print(f"{YLW}[!]{RST} '{filename}' size unknown")
            else:
                print(f"{GRN}[+]{RST} '{filename}' size: {file_size:.2f} MB")
            while True:
                q = input("Continue download? [Yes/No] ").lower().strip()
                if q == "yes" or q == "y":
                    print("")
                    break
                elif q == "no" or q == "n":
                    return f"{RED}[-]{RST} Download cancelled"
                else:
                    print(f"Error: Unknown input: '{q}'")
                    continue

        print(f"Status: {status_code} | File type: {file_type}")
        print(f"File name: {filename} [ {file_size:.2f} MB ]")
        print("")

        if args.directory:
            if os.path.isdir(args.directory):
                save_path = args.directory
            else:
                print(f"{YLW}Warning:{RST} Directory '{args.directory}' does not exist")
                print("Creating directory ...")
                print("")
                os.mkdir(args.directory)
                save_path = args.directory
        else:
            save_path = os.curdir

        print("--------------------------------------")

        print(f"Downloading: {filename} ...", end="\r")

        with open(f"{save_path}/{filename}", "wb") as file:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)
        
        return f"Downloading: {filename} ... {GRN}done{RST}"
    except KeyboardInterrupt:
        os.remove(f"{save_path}/{filename}")
        return f"Downloading: {filename} ... {YLW}canceled{RST}"
    except requests.exceptions.ConnectionError as e:
        return e
    except requests.exceptions.MissingSchema as e:
        return e


def info(response):
    print("")
    print("--START--")
    print(f"status: {response.status_code}")
    print("-" * 8 + "-" * len(str(response.status_code)))
    print(f"headers:")
    print("-" * 8)
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("--END--")


def banner():
    print(PROG)
    print("-" * len(PROG))


if __name__ == "__main__":
    main()
