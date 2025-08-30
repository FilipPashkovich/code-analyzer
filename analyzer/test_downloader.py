from downloader import download_repo

# test_downloader.py
from downloader import download_repo

ok, out = download_repo("https://github.com/pypa/sampleproject.git", "tmp_ok")
print(ok); print(out)

bad, out = download_repo("https://github.com/pypa/___nope___.git", "tmp_bad")
print(bad); print(out)
