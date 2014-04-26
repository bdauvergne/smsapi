from .ovh import OVH

if __name__ == '__main__':
    import argparse
    import sys
    import json

    carriers = {
            'ovh': OVH,
    }

    parser = argparse.ArgumentParser(description='Send SMS')
    parser.add_argument('--carrier', help='the carrier type', required=True)
    parser.add_argument('--params', action='append', help='comma separated options', default=[])
    parser.add_argument('--to', help='telephone numbers',
            action='append', required=True)
    args = parser.parse_args()
    kwargs = dict(param.split('=', 1) for param in args.params)
    carrier = carriers[args.carrier](**kwargs)
    content = sys.stdin.read()
    response = carrier.send_sms(args.to, content)
    print json.dumps(response, indent=4)


