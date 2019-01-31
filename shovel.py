#!/usr/bin/env python3

from asyncio import get_event_loop
from subprocess import run, PIPE
from argparse import ArgumentParser


class Shovel:

    def __init__(self):
        self.url_path: str = ""


    def arguments(self):
        try:
            args = ArgumentParser()
            args.add_argument("urls", help="Path to list of urls.")
            parsed = args.parse_args()
            return parsed
        except Exception as e:
            print("arguments: " + str(e))
            exit(1)


    def argument_parser(self):
        try:
            parsed = self.arguments()
            urls = parsed.urls
            if len(urls) < 200:
                self.url_path = urls
            else:
                print("Input length excessive.")
                exit(1)
        except Exception as e:
            print("argument_parser: " + str(e))
            exit(1)


    async def read_urls(self):
        try:
            with open(self.url_path, "r") as file:
                return [f for f in file.readlines()]
        except Exception as e:
            print("Error! in read_urls: " + str(e))
            exit(1)


    async def build_list(self, urls_list):
        try:
            plain_hosts = [u[7:] for u in urls_list]
            no_www = [u[:7]+u[11:] for u in urls_list]
            inc_no_www = urls_list + no_www
            inc_https = ["https" + u[4:] for u in inc_no_www]
            all = plain_hosts + inc_no_www + inc_https
            return [x.rstrip("\n") for x in all]
        except Exception as e:
            print("Error! in build_list: " + str(e))
            exit(1)


    async def dig(self, url: str):
        try:
            print("digging " + url)
            proc = run(["/usr/bin/dig " + url], stdout=PIPE, shell=True)
            proc.check_returncode()
            print(str(proc.stdout.decode()))
        except Exception as e:
            print("Error! in dig: " + str(e))
            exit(1)


    async def controller(self):
        try:
            self.argument_parser()
            full_list = await self.build_list(await self.read_urls())
            [await self.dig(f) for f in full_list]
        except Exception as e:
            print("Error! in controller: " + str(e))
            exit(1)


def main():
    try:
        loop = get_event_loop()
        loop.run_until_complete(loop.create_task(Shovel().controller()))
    except Exception as e:
        print("Error! in main: " + str(e))
        exit(1)


if __name__ == '__main__':
    main()

