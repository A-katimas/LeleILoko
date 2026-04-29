from parthing.parthing_folders import parse_file
import sys


def main():
    flyin = parse_file(sys.argv[1])
    print(flyin.connections[1])


if __name__ == "__main__":
    main()
