class AdvancedSearch {
    constructor(container_id, config_args = {}) {
        let config = {
            ...{
                "parameter_options": []
                // ,"search_parameter_elements": []
            },
            ...config_args
        };
        Object.assign(this, config);
        this.container_id = container_id;
        this.linkToHTML();
    }

    linkToHTML() {
        this.container_element = document.getElementById(this.container_id);
        this.container_element.classList.add("AdvancedSearchContainer");

        this.add_parameter_button = document.createElement("button");
        this.add_parameter_button.classList.add("AddParameterButton");
        this.add_parameter_button.textContent = "Add parameter"
        this.add_parameter_button.onclick = (event) => {
            console.log("Adding a search parameter!");
            this.addSearchParameter();
        };

        this.container_element.appendChild(this.add_parameter_button);
    }

    addSearchParameter() {
        let fragment = new DocumentFragment();
        let parameter_container = document.createElement("div");
        parameter_container.classList.add("SearchParameter");
        // parameter_container.id = `${this.container_id}_${}`
        fragment.appendChild(parameter_container);

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
        search_box.type = "text";
        search_box.classList.add("ParameterSearchBox");
        parameter_container.appendChild(search_box);

        let delete_button = document.createElement("button");
        delete_button.innerText = "Delete";
        delete_button.onclick = (event) => {
            this.container_element.removeChild(fragment);
        }
        parameter_container.appendChild(delete_button);

        this.container_element.appendChild(fragment);
        // this.search_parameter_elements.append(fragment);
    }
}