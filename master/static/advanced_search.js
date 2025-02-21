class AdvancedSearch {
    constructor(container_id, config_args = {}) {
        let config = {
            ...{
                "parameter_options": []
                ,"form_action": ""
                // ,"parameter_elements": []
            },
            ...config_args
        };
        Object.assign(this, config);
        this.container_id = container_id;
        this.linkToHTML();
        this.url_search_params = new URLSearchParams(window.location.search);
        this.number_of_parameters = 0;
        this.date_delimiters = {};
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

        this.form_element = document.createElement("form");
        this.form_element.classList.add("AdvancedSearchForm");
        this.form_element.action = this.form_action;
        this.container_element.appendChild(this.form_element);

        this.add_parameter_button = document.createElement("button");
        this.add_parameter_button.classList.add("AddParameterButton");
        this.add_parameter_button.textContent = "Add parameter"
        this.add_parameter_button.type = "button";
        this.add_parameter_button.onclick = (event) => {
            console.log("Adding a search parameter!");
            this.addSearchParameter();
        };
        this.form_element.appendChild(this.add_parameter_button);

        this.parameter_container_container = document.createElement("div");
        this.parameter_container_container.classList.add("ParameterContainer");
        this.form_element.appendChild(this.parameter_container_container);

        this.search_button = document.createElement("button");
        this.search_button.classList.add("SearchButton");
        this.search_button.type = "submit";
        this.search_button.disabled = true;
        this.search_button.textContent = "Search";
        this.form_element.appendChild(this.search_button);
    }

    addSearchParameter(option = null, value = null/*, type = "test"*/) {
        // let fragment = new DocumentFragment();

        let parameter_container = document.createElement("div");
        parameter_container.classList.add("SearchParameter");
        // parameter_container.id = `${this.container_id}_${}`
        // fragment.appendChild(parameter_container);

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
        }
        if (value) {
            input_element.name = option;
            input_element.value = value;
            parameter_select.value = option;
        }
        else if (this.parameter_options !== {}) {
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
            else {
                if (parameter_select_2 !== null) {
                    parameter_container.removeChild(parameter_select_2);
                    // parameter_select_2 = null;
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
}