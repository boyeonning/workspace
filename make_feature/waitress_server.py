import os
import app
import socket
import argparse

from loguru import logger
from waitress import serve

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    ip = s.getsockname()[0]
    return ip


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080, help='port number')
    parser.add_argument('--log_level', type=str, default='DEBUG',
                        choices=['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('--gpu', type=str, default='0', help='0, 1, 2, ...')
    parser.add_argument('--log_path', type=str, default='./log/')
    parser.add_argument('--revision', type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_argument()
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu

    ip_address = get_ip_address()
    args.ip_str = f'{ip_address}:{args.port}'

    log_path = args.log_path
    os.makedirs(log_path, exist_ok=True)
    logger.add(os.path.join(log_path, '{time:YYYY-MM-DD}.log'), level=args.log_level, rotation="00:00")

    logger.info(f'Make Feature API initializing at {args.ip_str} revision {args.revision}')

    mf = app.MakeFeature(args.revision)

    server_name = 'make_feature'
    mf.app.add_url_rule(f'/{server_name}', view_func=mf.api, methods=['POST'])
    logger.info(f'{server_name} API start serving at {args.ip_str} revision {args.revision}')
    serve(mf.app, host='0.0.0.0', port=args.port, threads=1)
