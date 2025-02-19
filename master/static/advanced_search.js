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
        for (const search_param of this.url_search_params) {
            if (search_param[0] !== "page") {
                this.addSearchParameter(search_param[0], search_param[1]);
            }
        }
        this.number_of_parameters = 0;
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

    addSearchParameter(option = null, value = null) {
        // let fragment = new DocumentFragment();

        let parameter_container = document.createElement("div");
        parameter_container.classList.add("SearchParameter");
        // parameter_container.id = `${this.container_id}_${}`
        // fragment.appendChild(parameter_container);

        let parameter_select = document.createElement("select");

        for (let parameter_option of this.parameter_options) {
            console.log(`Parameter option: ${parameter_option}`);
            let option_element = document.createElement("option");
            option_element.value = parameter_option;
            option_element.innerText = parameter_option;
            parameter_select.appendChild(option_element);
        }
        parameter_container.appendChild(parameter_select);

        let search_box = document.createElement("input");
        search_box.classList.add("ParameterSearchBox");
        search_box.type = "text";
        if (value) {
            search_box.name = option;
            search_box.value = value;
            parameter_select.value = option;
        }
        else if (this.parameter_options.length > 0) {
            search_box.name = this.parameter_options[0];
        }
        parameter_container.appendChild(search_box);

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
            search_box.name = parameter_select.value;
        }
        parameter_container.appendChild(delete_button);

        this.parameter_container_container.appendChild(parameter_container);
        ++this.number_of_parameters;
        this.search_button.disabled = false;

        // this.container_element.appendChild(fragment);
        // this.parameter_elements.append(parameter_container);
    }
}