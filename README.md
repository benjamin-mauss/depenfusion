![Untitled](https://user-images.githubusercontent.com/86640585/135770826-57d80968-675a-40fd-a156-b0b7fa08e972.png)


The pentest tool made for find depencency confusion vulnerabilities in node js.

## What is DepenFusion?

DepenFusion is a multithread <a href="https://en.wikipedia.org/wiki/Penetration_test">pentest</a> tool made for find <a href="https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610">depencency confusion</a> vulnerabilities in node js (npm).

## How to use?

This tool is easy to use.
You must provide the subdomains/domains you want to analyse in the <a href="https://www.howtogeek.com/435903/what-are-stdin-stdout-and-stderr-on-linux/">stdin</a>.

Example:

```bash
cat subdomains.txt | python3 ./main.py
```

## How to install?

- First, you make sure that you have git and python3 installed.
- Download the tool using the command

```bash
git clone github.com/gato-louco-cv/depenfusion
```

- Change the directory to depenfusion

```bash
cd depenfusion
```

- Install the depencencies using

```bash
pip3 install -r requirements.txt
```

- Run the program using

```bash
cat subdomains.txt | python3 ./main.py
```

## Advanced usage

You may want to check --help.

```bash
$ python3 ./main.py --help
usage: main.py [-h] [-th TH] [-to TO] [-a A] [-v V] [--version] [-s] [-link] [-p]

Get subdomains from stdin and search for dependency confusion.

optional arguments:
  -h, --help  show this help message and exit
  -th TH      Number of concurrence threads (default=10)
  -to TO      Timeout (in seconds) (default=15)
  -a A        String to append in the end of url. E.g: -a="?token=foo" (default="")
  -v V        Verbose mode (0 to 3) (default=0))
  --version   Show version and exit
  -s          Silent, only shows the useful results (default=False)
  -link       Show full link to the npm possible vulnerable package (default=False)
  -p          Not include the path provided in the url (default=False, include the path)
```

## Good to know

This tool is smart. If you provide

```txt
https://controls.platform.account.www.microsoft.com
http://controls.platform.account.www.microsoft.com/
controls.platform.account.www.microsoft.com/
controls.platform.account.www.microsoft.com/private
controls.platform.account.www.microsoft.com/private/
```

Both are going to work fine.
If you use the `-p` option, the path won't be included. So, in the example above, `/private` and `/private/` are going to be ignored.

Also, `-s` is intent to be used if you are using depenfusion along with ther tool.

## How it works

Basically it:

- Async Request to the target appending `package.json` and `package-lock.json` to the url.
- Check if it is a valid file. If so, extract the dependencies.
- Request to npm api check if the dependencies exist.

## Future

- Support pip (python) and gem (ruby)
- Make it using GoLang
