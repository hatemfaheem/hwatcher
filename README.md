# hwatcher
A directory monitoring daemon manager uploading to S3.

hwatcher creates passive monitors for specified directories and upload new created files to the specified bucket on S3.

You can do 3 things:
- Start a new daemon.
- Killing a daemon.
- Listing all daemons running on our machine.

This project is based on pyinotify
https://github.com/seb-m/pyinotify
