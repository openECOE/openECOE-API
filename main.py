import argparse

from src.apps.manage.boot import boot as boot_manage


service_mapping = {
    'manage': boot_manage,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--service',
        type=str,
        nargs='?',
        help='Service to run must be one of ["manage"]',
    )
    params = vars(parser.parse_args())
    service_name = params['service']
    service_booter = service_mapping[service_name]

    print(f'Booting {service_name} server')
    service_booter()
    print(f'{service_name} server start success')
