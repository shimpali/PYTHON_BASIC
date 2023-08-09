# **Capstone Project**

You will create a console utility for generating test data based on the provided data schema.

**Project description:**

Imagine that you have a data pipeline and you need some test data to check correctness of data transformations and validations on this data pipeline.

You need to generate different input data.

In our Capstone project we will solve it by creating a universal console utility that will generate our data for us. Format - only JSON.

Create all descriptions, names for commands, etc by yourself.

**You need to implement (**⚠️ **please learn new materials with following links):**

**Name, description, help.** Console Utility (CU) must have a name. You need to set a name on it and the name must be shown in “help”. Each command must have a help. Use argparse to get all those features from the box.

More about argparse: [https://docs.python.org/3/library/argparse.html](https://docs.python.org/3/library/argparse.html)

**All params could be set up from cmd (command line).** CU must take all params needed to generate data from the command line, but most of them must have default values.

**Default values.** All params for CU must have default values. All those values must be shown in CU help. All default values must be stored in the “default.ini” file and read from it with configparser. Names of options in default.ini must be identical to those options in console utility help.

More about configparser: [https://docs.python.org/3/library/configparser.html](https://docs.python.org/3/library/configparser.html)

**Logging.** All steps must have output in the console. If you’ve got some error, you must print it to the console with logging.error and only after that exit. If you start data generating - you need to write about it in the console, same if you finish. All logs must be printed in the console. If you want to, you can also duplicate all logs in a log file, but it is optional for this project.

More about logging: [https://docs.python.org/3/howto/logging.html#logging-basic-tutorial](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)

**Random data generation depends on field type and data schema.** Described in detail in “Data Schema Parse” point.

**Parallelism**. Use multiprocessing to add the ability to speed up file generation.

**Data Schema Parse:**

Your script must parse data schema and generate data based on it. All keys in data schema == keys in the final data event line.

**Example of data schema:**

{“date”:”timestamp:”, “name”: “str:rand”, “type”:”str:[‘client’, ‘partner’, ‘government’]”, “age”: “int:rand(1, 90)”}

**All values support special notation “type:***what_to_generate*”:

“:” in value indicates that the left part of the value is a type.

**Type could be:** timestamp, str and int.

If in schema there is another type on the left part of the “:” statement in value, write an error.

**For example**, “str:rand” means that the value of this key must be a str type and it’s generated randomly.

**For right part of values with “:” notation, possible 5 options:**

1. **rand** - random generation, if on the left there is “**str**” type, for generation use uuid4 (need to use only one function to generate uuid prefix - [https://docs.python.org/3.6/library/uuid.html#uuid.uuid4](https://docs.python.org/3.6/library/uuid.html#uuid.uuid4)), str(uuid.uuid4())
    - If on the left there is “**int**” type, use random.randint(0, 10000)
2. **list with values []**. For example, ”str:[‘client’, ‘partner’, ‘government’]” or “int:[0, 9, 10, 4]”. Generator must take a random value from a list for each generated data line. Use random.choice.
3. **rand(from, to)** - random generation for int values in the prescribed range. Possible to use only with “int” type. If on the left part “str” or “timestamp”, write an error.
4. **Stand alone value**. If in schema after “:” a value is written, which has a type corresponding with the left part, and the word “**rand**” is not reserved, use it on each line of generated data. For example, “name”: “str:cat”. So your script generates data where in each line attr “name”:”cat” will be. But if in schema there is “age”:”int:head”, it is an error and you must write about it in the console, because “head” could not be converted to int type.
5. **Empty value.** It’s normal for any type. If type “int” is with empty value, use None in value, if type “str”, use empty string - “”.

**For timestamp type** - ignore all values after “:”. If value exists in scheme, write logging.warning with a note that timestamp does not support any values and it will be ignored. Continue correct script work. **Value for timestamp is always the current unix timestamp** - enough to use time.time().

**List of input params for CU:**

- *Name and Description you can freely change

| Name** | Description*                                                                                                                                                                                                                  | Behavior                                                                                                                                                                                                                                                       |
| --- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| path_to_save_files | Where all files need to save                                                                                                                                                                                                  | User can define a path in 2 ways: relatively from cwd (current working directory) and absolute. You CU must correct work with both ways and check if such path or not. If path exist and it is not a directory - exit with error log. `.` - means current path |
| files_count | How much json files to generate                                                                                                                                                                                               | if files_count < 0 - error, if files_count == 0 - print all output to console.                                                                                                                                                                                 |
| file_name | Base file_name. If there is no prefix, the final file name will be file_name.json. With prefix full file name will be file_name_file_prefix.json                                                                              |                                                                                                                                                                                                                                                                |
| file_prefix | What prefix for file name to use if more than 1 file needs to be generated                                                                                                                                                    | prefix is a set of possible choices (https://docs.python.org/3.6/library/argparse.html#choices) :- count -random -uuid (need to use only one function to generate uuid prefix - https://docs.python.org/3.6/library/uuid.html#uuid.uuid4, str(uuid.uuid4()))   |
| data_schema | It’s a string with json schema. It could be loaded in two ways: 1. With path to json file with schema 2. with schema entered to command line.Data Schema must support all protocols that are described in “Data Schema Parse” | Read schema and check if it’s correct or not (see “Data Schema Parse” with details of schema).                                                                                                                                                                 |
| data_lines | Count of lines for each file. Default, for example: 1000.                                                                                                                                                                     |                                                                                                                                                                                                                                                                |
| clear_path | If this flag is on, before the script starts creating new data files, all files in path_to_save_files that match file_name will be deleted.                                                                                   | If this flag is on, store true (https://docs.python.org/3.6/library/argparse.html#action , see action='store_true')                                                                                                                                            |
| multiprocessing | The number of processes used to create files. Divides the “files_count” value equally and starts N processes to create an equal number of files in parallel. Optional argument. Default value: 1. | If multiprocessing < 0 - error, if multiprocessing > os.cpu_count() - replace input value to os.cpu_count() os.cpu_count() is used to get the number of CPUs in the system.                                                                                    |

**Example of CU launch with provided data_schema from cmd (“magicgenerator - pseudo name of CU):**

$ magicgenerator . --file_count=3 --file_name=super_data --prefix=count --multiprocessing=4 --data_schema="{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"

**Data schema from file:**

$ magicgenerator . --file_count=3 --file_name=super_data --prefix=count --data_schema=./path/to/schema.json

**Do not use Traceback errors and raise!** If it’s a console utility, it must have the corresponding behavior. You do not need to send Interpreter traceback or raise errors. All errors that cause exit from script must be processed with “sys.exit(1)” or “exit(1)”, not with raise.

**You need to use:**

Argparse, JSON, os/shutil, time, random, configparser, logging, uuid, pytest, multiprocessing

**CU result:**

**Those data schema:**

{“date”:”timestamp:”, “name”: “str:rand”, “type”:”[‘client’, ‘partner’, ‘government’]”, “age”: “int:rand(1, 90)”}

**Expected result:**

{"date":"1534717897.967033", "name": "f82a44ac-daa7-4b8f-8569-83898fb9b312", "type":" partner", "age": 45}

{"date":"1534717898.442959", "name": "660ddea3-cbe4-47cf-918f-bafec6e87951", "type":"government", "age": 12}

{"date":"1534717896.136228", "name": "0c8ccb4b-2b5c-4a50-ad46-b0e08f7f8448", "type":"client", "age": 61}

All params must work correctly and create the expected result: each file must have a number of lines == data_lines and etc. In case of file output result file should be in [https://jsonlines.org/](https://jsonlines.org/)

If something is not described in this white paper, do it as you think appropriate.

**Testing:**

- Write a parameterized test for different data types.
- Write a parameterized test for different data schemas.
- Write a test that uses temporary files to test your program when the data schema is loaded with a json file. You have to use fixtures here.
- Test for the “clear_path” action.
- Test to check saving file to the disk.
- Write a test to check a number of created files if “multiprocessing” > 1.
- Write your own test.

**Acceptance Criteria:**

- All features are implemented and work.
- All possible errors are processed and they have a logging and correct exit (impossible to create file, incorrect values, etc.).
- Code must be divided into functions/classes/ logic blocks. It must not be a monolit sheet of code.
- Unit tests exist.
- All steps from the Project Checklist module are done.

---

## Commands

### Create venv
- python3 -m venv env_name

### Activate venv
- source env_name/bin/activate


### Install Packages
- pip3 install -r requirements.txt
