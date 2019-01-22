import yaml
import pathlib


def yaml_parser(yaml_file: str):
    print(yaml_file)
    with open(yaml_file, 'r') as stream:
        try:
            parameter_dict = yaml.load(stream)
            print(parameter_dict)
            return parameter_dict
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':

    yaml_file = "config/test.yaml"
    yolo = yaml_parser(yaml_file)
    print("========================================")
    print(yolo)

    print("!!!========================================!!!")
    print("!!!========================================!!!")

    yaml_file = pathlib.Path('config/test.yaml').absolute()
    yolo = yaml_parser(yaml_file)
    print("========================================")
    print(yolo)
