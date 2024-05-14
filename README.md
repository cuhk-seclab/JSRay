# JSRay

This is the artifact for our WWW'24 paper: **[Detecting and Understanding Self-Deleting JavaScript Code](https://dl.acm.org/doi/10.1145/3589334.3645540)**.

## Environment

- Debian 9 (may also work on newer version, but not tested)
- At least 200GB of free disk space
- gcc version 6.3.0 20170516 (Debian 6.3.0-18+deb9u1) (may also work on newer version, but not tested)

## Build

Check [official document](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md) if you meet any problem.

Install depot_tools
```
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
# change to your own path
export PATH="$PATH:/path/to/depot_tools"
```

Get code
```
mkdir chromium && cd chromium
fetch --nohooks chromium
# have a cup of coffee
cd src
git checkout -b dev 96.0.4664.45
# If you miss build dependencies, try this
# ./build/install-build-deps.sh
gclient runhooks
```

Patch
```
cd third_party/blink
# change to your path
git apply /path/to/0001-jsray-blink.patch
cd ../../v8
# change to your path
git apply /path/to/0001-jsray-v8.patch
cd ../
```

Build
```
gn gen out/Default '--args=cc_wrapper="ccache" is_debug=false enable_nacl=false'
time autoninja -C out/Default/ chrome
```

## Test
```
mkdir -p script
/path/to/chrome --headless --no-sandbox --user-data-dir=profile file:///path/to/example/simple.html
```
Output will be logged in `out.log` with script activities. All captured scripts can be found at `script/`. If there is any warning in the output, delete operation is performed. By tracing IDs in the log, we can further identify self-deleting scripts.

Please note that using `file://` is for demonstration only!

## Other folders

- [evaluation](evaluation): contains our collected data for reproducing the results of the paper.
- [figure](figure): contains scripts to collect all figures in the paper.
- [scripts](scripts): contains scripts for automatic evaluation.

## License

JSRay is under [MIT License](LICENSE).

## Publication

You can find more details in our WWW'24 paper.

```
@inproceedings{10.1145/3589334.3645540,
author = {Wang, Xinzhe and Zhuang, Zeyang and Meng, Wei and Cheng, James},
title = {Detecting and Understanding Self-Deleting JavaScript Code},
year = {2024},
booktitle = {Proceedings of the ACM on Web Conference 2024},
pages = {1768–1778},
numpages = {11},
series = {WWW '24}
}
```

## Contact
- Xinzhe Wang (xzwang21@cse.cuhk.edu.hk)
- Zeyang Zhuang (zyzhuang22@cse.cuhk.edu.hk)
- Wei Meng (wei@cse.cuhk.edu.hk)
- James Cheng (jcheng@cse.cuhk.edu.hk)