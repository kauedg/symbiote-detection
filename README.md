# Symbiote Malware Detection
Guidelines for detecting and disabling Symbiote malware on Linux. Check [this article](https://blogs.blackberry.com/en/2022/06/symbiote-a-new-nearly-impossible-to-detect-linux-threat) for other filenames used and more detailed information.

## First steps
Due to the malware's ability to tamper syscalls by hooking system libraries, you can't rely on dynamically compiled tools (e.g. your regular `ls`, `find` and such). Download the [pre-compiled and static linked busybox](https://busybox.net/downloads/binaries/) to workaround this problem:

```shell
$ curl -s https://busybox.net/downloads/binaries/1.35.0-i686-linux-musl/busybox -o busybox && chmod +x busybox && ./busybox | head -n1 
BusyBox v1.35.0 (2022-01-17 18:45:13 CET) multi-call binary.
```


There's more than one version of this malware and I've seen two of them, each with it's set of filenames. But three things are certain:

#### 1) C Headers (`.h`) files should never be of filetype "data":
Look for these files in your system by running the command below and if it outputs you any `.h` file having `data` type, it's almost certain it contains captured ssh credentials 

(run all commands below as the `root` user)

```shell
$ ./busybox find / -type f -iname "*.h" -exec file {} \; | /busybox grep -v "text|magic"
/usr/include/linux/usb/usb.h: data
```
Up to now, I'm aware of two of these files:
- `/usr/include/linux/usb/usb.h` (from an older version - check the decoder in this repository)
- `/usr/include/certbot.h`

#### 2) If you don't know why you have a `/etc/ld.so.preload` file, you probably shouldn't have one:
```shell
$ ./busybox cat /etc/ld.so.preload
/lib64/init.so
```
If you remove the preload file, your regular dynamically linked binaries may work again, but they're not trustworthy anymore. You may also remove the library pointed by it (don't forget to copy to a backup for later analysis, if needed).

#### 3) Your libraries shouldn't have the string "rootkit" in it:
```shell
$ ./busybox strings /lib64/init.so | ./busybox grep "rootkit"
rootkit.c
```

By now if any of this commands returned output indicating the presence of the Symbiote, you may rename your host to `eddie_brock` :)

#### Processes
Use `busybox` to look for processes named `kernelconfig`, `kerneldev` or `dbuss` 
```shell
$ ./busybox ps aux | ./busybox grep -E "kernelconfig|kerneldev|dbuss"
```
Also check for programs in listener mode on some high port.
```shell
$ ./busybox netstat -lpa | ./busybox grep -E "kernelconfig|kerneldev|dbuss"
```


#### File collecting for analysis
It's recommended that you backup any malware related file, specially the `.h` files with captured credentials. Don't forget to use busybox's `cp` with the `-p` switch to preserve files' `stat` information. This may give you precious tips on the timeline of events, like since when it's there and when it was last modified.

