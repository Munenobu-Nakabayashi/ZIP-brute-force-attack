import argparse
import itertools
import os
import string
import sys
import zipfile

def create_parser():
    parser = argparse.ArgumentParser(description='Password Cracker for ZIP archived file.',
                                     epilog="If you don't use optional arguments, target set is upper case and lower case (A-Za-z).")
    parser.add_argument("zipfile", action='store', help='zipfile')
    parser.add_argument("length", action='store', type=int, default=5, help='the length of password. Default value is 5.')
    parser.add_argument("-d", "--digits", action='store_true', help='append digits to target set.')
    parser.add_argument("-l", "--lower", action='store_true', help='append lower case to target set.')
    parser.add_argument("-p", "--punctuation", action='store_true', help='append punctuation to target set.')
    parser.add_argument("-u", "--upper", action='store_true', help='append upper case to target set.')
    parser.add_argument("-w", "--white", action='store_true', help='append whitespace to target set.')
    return parser

def create_target_strings(args):
    target_chars = ""
    if not any((args.digits, args.lower, args.punctuation, args.upper, args.white)):
        target_chars = string.ascii_lowercase + string.ascii_uppercase
    else:
        if args.digits:
            target_chars += string.digits
        if args.lower:
            target_chars += string.ascii_lowercase
        if args.punctuation:
            target_chars += string.punctuation
        if args.upper:
            target_chars += string.ascii_uppercase
        if args.white:
            target_chars += string.whitespace
    return target_chars

def extract_zip(args, target_chars):

    with zipfile.ZipFile(args.zipfile, 'r') as zf:
        zf.extractall(os.path.splitext(sys.argv[1])[0], pwd=password.encode())

def crack_password(args, target_chars):
    target_iter = itertools.chain([""], itertools.product(target_chars, repeat=args.length))
    for challenge in target_iter:
        try:
            password = "".join(challenge).encode()
            extract_zip(args, challenge)
            print('PASS:', "".join(challenge))
            break
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
        except RuntimeError:
            pass

def main():
    parser = create_parser()
    args = parser.parse_args()
    target_chars = create_target_strings(args)
    crack_password(args, target_chars)

if __name__ == '__main__':
    main()