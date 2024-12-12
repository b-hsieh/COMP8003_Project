from argparse import ArgumentParser, Namespace, ArgumentTypeError
from socket import error, inet_aton


def positive_int(value):
    ivalue = int(value)
    if ivalue < 0:
        raise ArgumentTypeError('%s is an invalid positive integer' % value)
    return ivalue


def string(value):
    if isinstance(value, str):
        return value
    raise ArgumentTypeError('%s is not a string' % value)


def valid_ip_address(value):
    try:
        inet_aton(value)
        return value
    except error:
        raise ArgumentTypeError('%s is not a valid IP address' %value)


def _victim_parse_arguments() -> Namespace:
    parser = ArgumentParser(description='Victim arguments')
    parser.add_argument(
        "ip_address", type=valid_ip_address, help="IP Address of the Victim"
    )
    parser.add_argument("port", type=positive_int, help="Port number for the victim")

    return parser.parse_args()


def _attacker_parse_arguments() -> Namespace:
    parser = ArgumentParser(description='Attacker arguments')
    parser.add_argument(
        "ip_address", type=valid_ip_address, help="IP Address of the Victim"
    )
    parser.add_argument("port", type=positive_int, help="Port number for the Victim")
    parser.add_argument("command", type=string, help="Command for the Victim to run")
    return parser.parse_args()


def attacker_parse_arguments():
    args = _attacker_parse_arguments()
    return args.ip_address, args.port, args.command


def victim_parse_arguments():
    args = _victim_parse_arguments()
    return args.ip_address, args.port