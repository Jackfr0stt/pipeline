## Requirements

This convertion has the following requirements:

- `Python3`, at least, version 3.7 - `sudo apt install python3`
- `rdflib`, library to convert OWL to JSON - `sudo apt install rdflib`

You can also use the following command to do every command in one fell swoop:

- `sudo apt update && sudo apt install python3 && sudo apt install rdflib`

## Commands

To run the script simply input the following command:

- `bash script.sh` - converts OWL file to DDL

## Generated files

The following files are generated according to file name:

- `<OWL_FILE>.json`
- `<OWL_FILE>.ddl`

