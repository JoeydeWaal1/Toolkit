import argparse
import sys

# cmd line argumenten parsen
def get_arguments():
    parser = argparse.ArgumentParser()

    # scan mode
    parser.add_argument("-s", "--scan") # scan mode
    parser.add_argument("-c", "--card")  # welke interface er gescaned moet worden

    # attack mode
    parser.add_argument("-a", "--attack")#, action="store_true")

    # hostname/ip
    parser.add_argument("-t", "--target")
    parser.add_argument("-g", "--gateway")
    parser.add_argument("--host")

    parser.add_argument("-o", "--output")
    if len(sys.argv)==1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()
    return args
