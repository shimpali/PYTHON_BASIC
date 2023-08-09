import json


def load_data_schema_from_args(args) -> dict | str:
    try:
        data = json.loads(args.data_schema)
        return data
    except json.decoder.JSONDecodeError as e:
        message = e.msg
        return message


def dump_data_to_json_file(path: str, data) -> None:
    with open(path + '.jsonl', 'a') as file:
        for record in data:
            file.write(f'{json.dumps(record)}\n')
