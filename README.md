# hwatcher
A directory monitoring daemon manager uploading to S3.

hwatcher creates passive monitors for specified directories and upload new created files to the specified bucket on S3.

You can consider this a tiny version of dropbox for developers that takes files automatically to S3 to be part of other complex processes on AWS. You can think of this as a micro step towards automation.

hwatcher currently supports 3 actions:
- Start a new daemon.
- Killing a daemon.
- Listing all daemons running on our machine.

Dependencies:
- Python 2.7
- pyinotify https://github.com/seb-m/pyinotify
- boto3 https://github.com/boto/boto3
