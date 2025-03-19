class AdvancedSearch {
    constructor(container_id, config_args = {}) {
        let config = {
            parameter_options: []
            ,json: []
            ,tbody_object: null
            // ,search_action: () => {console.log(`No search action defined for advanced search of ${container_id}`)}
            // ,"form_action": ""
            // ,"parameter_elements": []
        };
        Object.assign(this, config, config_args);
        this.container_id = container_id;
        this.linkToHTML();
        this.url_search_params = new URLSearchParams(window.location.search);
        this.number_of_parameters = 0;
        this.date_delimiters = {};
        this.active_parameters = {};
        for (const [parameter_option, type] of Object.entries(this.parameter_options)) {
            if (type === "date") {
                this.date_delimiters[parameter_option] = "At";
            }
        }
        for (const [search_param_option, search_param_value] of this.url_search_params) {
            if (search_param_option.endsWith("delimiter")) {
                let search_param_option_truncated = search_param_option.substring(0, search_param_option.indexOf("delimiter") - 1);
                this.date_delimiters[search_param_option_truncated] = search_param_value;
            }
            else if (search_param_option !== "page") {
                this.addSearchParameter(search_param_option, search_param_value);
            }
        }
    }

    linkToHTML() {
        this.container_element = document.getElementById(this.container_id);
        this.container_element.classList.add("AdvancedSearchContainer");

        this.add_parameter_button = document.createElement("button");
        this.add_parameter_button.classList.add("AddParameterButton");
        this.add_parameter_button.textContent = "Add parameter"
        this.add_parameter_button.type = "button";
        this.add_parameter_button.onclick = (event) => {
            console.log("Adding a search parameter!");
            this.addSearchParameter();
        };
        this.container_element.appendChild(this.add_parameter_button);

        this.parameter_container_container = document.createElement("div");
        this.parameter_container_container.classList.add("ParameterContainer");
        this.container_element.appendChild(this.parameter_container_container);

        this.search_button = document.createElement("button");
        this.search_button.classList.add("SearchButton");
        this.search_button.disabled = true;
        this.search_button.textContent = "Search";
        this.search_button.onclick = this.doSearch;
        this.container_element.appendChild(this.search_button);
    }

    addSearchParameter(option = null, value = null/*, type = "test"*/) {
        // TODO update URL on search without refreshing webpage
        // TODO search by date
        // let fragment = new DocumentFragment();

        let parameter_container = document.createElement("div");
        parameter_container.classList.add("SearchParameter");
        // parameter_container.id = `${this.container_id}_${}`
        // fragment.appendChild(parameter_container);

        // Drop down menu of what column to search
        let parameter_select = document.createElement("select");
        for (const [parameter_option, type] of Object.entries(this.parameter_options)) {
            console.log(`Parameter option: ${parameter_option}`);
            let option_element = document.createElement("option");
            option_element.value = parameter_option;
            option_element.innerText = parameter_option;
            parameter_select.appendChild(option_element);
        }
        parameter_container.appendChild(parameter_select);
        let parameter_select_2 = null;

        // Generates one or two input elements depending on the parameter type.
        // strings use one text box, dates use a date picker and a drop-down "select" element
        let input_element = document.createElement("input")
        if (option !== null && this.parameter_options[option].type === "date") {
            input_element.classList.add("ParameterDateBox");
            input_element.type = "date";
            parameter_select_2 = document.createElement("select");
            ["At", "Before", "After"].forEach(delimiter => {
                let temp_option_element = document.createElement("option");
                temp_option_element.value = delimiter;
                temp_option_element.innerText = delimiter;
                parameter_select_2.appendChild(temp_option_element);
            });
            parameter_select_2.name = option + "-delimiter";
            parameter_select_2.value = this.date_delimiters[option];
            parameter_select.insertAdjacentElement("afterend", parameter_select_2);
        }
        else {
            input_element.classList.add("ParameterSearchBox");
            input_element.type = "text";
            input_element.onchange = this.doSearch;
            this.active_parameters[name] = value; // Only works for strings
        }
        if (value) {
            input_element.name = option;
            input_element.value = value;
            parameter_select.value = option;
        }
        else if (this.parameter_options !== {}) {
            // When "add parameter" button is clicked it always sets the constraint to column 1. maybe change this
            input_element.name = Object.keys(this.parameter_options)[0];
        }
        parameter_container.appendChild(input_element);

        let delete_button = document.createElement("button");
        delete_button.classList.add("DeleteParameterButton")
        delete_button.innerText = "Delete";
        delete_button.onclick = (event) => {
            this.parameter_container_container.removeChild(parameter_container);
            --this.number_of_parameters;
            if (this.number_of_parameters < 1) {
                this.search_button.disabled = true;
            }
        }
        parameter_select.onchange = (event) => {
            let new_value = parameter_select.value;
            let new_type = this.parameter_options[new_value].type;
            // if (this.parameter_options[parameter_select.value].type === "date") {
            //     input_element.type = "date";
            // }
            input_element.type = new_type;
            input_element.name = new_value;
            if (new_type === "date") {
                parameter_select_2 = document.createElement("select");
                // parameter_select_2.name = "date_delimiter";
                ["At", "Before", "After"].forEach(delimiter => {
                    let temp_option_element = document.createElement("option");
                    temp_option_element.value = delimiter;
                    temp_option_element.innerText = delimiter;
                    parameter_select_2.appendChild(temp_option_element);
                });
                parameter_select_2.name = new_value + "-delimiter";
                parameter_select.insertAdjacentElement("afterend", parameter_select_2);
            }
            else { // Assuming we're switching from "date" to "string" search type
                // remove the select element
                if (parameter_select_2 !== null) {
                    parameter_container.removeChild(parameter_select_2);
                }
            }
        }
        parameter_container.appendChild(delete_button);

        this.parameter_container_container.appendChild(parameter_container);
        ++this.number_of_parameters;
        this.search_button.disabled = false;

        // this.container_element.appendChild(fragment);
        // this.parameter_elements.append(parameter_container);
    }

    doSearch() {
        // TODO ignore unchanged parameters

        this.tbody_object.populate();
    }
}