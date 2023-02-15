#!/bin/bash
set -e

json="APIbuster.json"
modelledJSON="APIbusterModelled.json"
modelledJSON2="APIbusterModelled2.json"
ddl="APIbuster.ddl"

# json="peopleOntology.json"
# modelledJSON="peopleOntologyModelled.json"
# modelledJSON2="peopleOntologyModelled2.json"
# ddl="peopleOntology.ddl"

info() {
    msg="\e\n[1;33;44m ===> $1 \e[0m"
    [ "$2" != "nobreak" ] && msg="${msg}\n"
    echo -n -e $msg
}

convert_OWL() {
    info "OWL --> JSON"
    python3 json_convert.py > $json

    info "$json was created."
}

model_JSON() {
    info "Modelling JSON file.."
    python3 json_modelling.py > $modelledJSON

    info "JSON file as been modeled."
}

convert_camel_case() {
    info "Converting strings from JSON file to camelCase.."
    python3 convert_camel_case.py > $modelledJSON2

    info "JSON file as been updated."
}

matchScript() {
    info "Building DDL file"
    python3 matchScript.py > $ddl

    info "Congratulations, DDL file is ready to be used."
}

cleanTheHouse() {
    if [ -f "$modelledJSON2" ]; then
        info "Thank you for using the conversion pipeline!"
        rm $modelledJSON2
    fi
}

main() {
    info "Starting conversion.."
    # converting OWL --> JSON
    convert_OWL
    # modelling JSON file
    model_JSON
    # converts strings in JSON file to camelCase
    convert_camel_case
    # builds ddl file based on JSON file
    matchScript
    # deletes files not used
    # cleanTheHouse
}

main