class Table {
    constructor(container_id, options = {}) {
        Object.assign(this, {
            page: 1
            ,json: []
            ,columns: {} // display_name, type
            ,alias: container_id
            ,json_url: null
        }, options);
        this.container_element = document.getElementById(container_id);
        this.advanced_search_container_element = document.createElement("div");
        this.pagination_container_element = document.createElement("div");
        this.table_element = document.createElement("table");
        this.thead_element = document.createElement("thead");
        this.tbody_element = document.createElement("tbody");

        // Add column headers
        let header_row_element = document.createElement("tr");
        for (let column of Object.values(this.columns)) {
            let column_element = document.createElement("th");
            column_element.innerText = column.display_name;
            header_row_element.appendChild(column_element);
        }
        this.thead_element.appendChild(header_row_element);

        this.table_element.appendChild(this.thead_element);
        this.table_element.appendChild(this.tbody_element);
        this.container_element.appendChild(this.advanced_search_container_element);
        this.container_element.appendChild(this.pagination_container_element);
        this.container_element.appendChild(this.table_element);

        // Generate pagination buttons
        this.previous_page_button = document.createElement("button");
        this.previous_page_button.textContent = "Previous";
        this.previous_page_button.onclick = () => {this.setPage(this.page - 1)};
        this.next_page_button = document.createElement("button");
        this.next_page_button.textContent = "Next";
        this.next_page_button.onclick = () => {this.setPage(this.page + 1)};
        this.previous_page_button.disabled = this.page === 1;
        this.next_page_button.disabled = this.page * entries_per_page > this.json.length;
        this.pagination_container_element.appendChild(this.previous_page_button);
        this.pagination_container_element.appendChild(this.next_page_button)

        if (this.json.length === 0 && this.json_url !== null) {
            this.tbody_element.textContent = "Fetching data...";
            this.refresh();
        }
        else {
            this.populate();
        }
    }
    populate() {
        // Delete existing rows if there are any
        while (this.tbody_element.lastChild) {
            this.tbody_element.removeChild(this.tbody_element.lastChild);
        }
        let start_index = (this.page - 1) * entries_per_page;
        let until_index = this.page * entries_per_page;
        if ((this.page - 1) * entries_per_page >= this.json.length) {
            this.tbody_element.textContent = "No data found.";
        }
        else {
            for (let i = start_index; i < until_index && i < this.json.length; i++) {
                let json_row = this.json[i];
                let table_row_element = document.createElement("tr");
                for (let column of Object.keys(this.columns)) {
                    let cell_element = document.createElement("td");
                    cell_element.textContent = json_row[column];
                    table_row_element.appendChild(cell_element);
                }
                this.tbody_element.appendChild(table_row_element);
                // table_row_element.onclick = () => {
                //     console.log(`Username: be like ${json_row.username}`);
                // }
            }
        }
        this.updatePageButtons();
    }
    setPage(page) {
        // if (page > 0 && (page-1) * entries_per_page < this.json.length) {
            this.page = page;
            this.populate();
        // }
        // else {
        //     throw(`Attempt to navigate to page ${page} in table ${this.alias} failed because it goes outside the bounds of the data`);
        // }
    }
    updatePageButtons() {
        this.previous_page_button.disabled = this.page === 1;
        this.next_page_button.disabled = this.page * entries_per_page >= this.json.length;
    }
    async refresh() {
        const response = await fetch(this.json_url);
        console.log(response);
        if (!response.ok) {
            this.tbody_element.textContent = "There was a problem fetching the data";
        }
        else {
            this.json = await response.json();
            this.populate();
        }
    }
}
/*
class AdvancedSearchTable extends Table {
    constructor(tbody_id, pagination_container_id, advanced_search_container_id, options = {}) {
        super(tbody_id, pagination_container_id, options);
        this.advanced_search_container_id = advanced_search_container_id;
        this.linkToHTML();
        this.url_search_params = new URLSearchParams(window.location.search);
        this.number_of_parameters = 0;
        // this.date_delimiters = {};
        this.active_parameters = {};
        for (const [parameter_option, properties] of Object.entries(this.parameter_options)) {
            // if (type === "date") {
                // this.date_delimiters[parameter_option] = "At";
            // }
            // else
                if (properties.type === "number") {
                console.log("type number");
                for (let i = 0; i < this.json.length; i++) {
                    this.json[i][parameter_option] = Number(this.json[i][parameter_option]);
                }
            }
        }
        this.initial_json = this.json;
        for (const [search_param_option, search_param_value] of this.url_search_params) {
            if (search_param_option.endsWith("delimiter")) {
                let search_param_option_truncated = search_param_option.substring(0, search_param_option.indexOf("delimiter") - 1);
                // this.date_delimiters[search_param_option_truncated] = search_param_value;
            }
            else if (search_param_option !== "page") {
                this.addSearchParameter(search_param_option, search_param_value);
            }
        }
    }
    linkToHTML() {
        this.container_element = document.getElementById(this.advanced_search_container_id);
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
        // this.search_button.disabled = true;
        this.search_button.textContent = "Search";
        this.search_button.onclick = () => { this.doSearch() };
        this.container_element.appendChild(this.search_button);
    }

    addSearchParameter(option = null, value = null) {
        // let fragment = new DocumentFragment();
        // When "new parameter" button clicked, it just adds the constraint to the first column
        if (option === null) {
            option = Object.keys(this.parameter_options)[0];
        }

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

        let input_element;
        // Generates one or two input elements depending on the parameter type.
        // strings use one text box, dates use a date picker and a drop-down "select" element
        if (this.parameter_options[option].type === "date" || this.parameter_options[option].type === "number" || this.parameter_options[option].type === "boolean") {
            if (this.parameter_options[option].type !== "boolean") {
                input_element = document.createElement("input");
                input_element.type = this.parameter_options[option].type;
            }
            // input_element.classList.add("ParameterDateBox");
            parameter_select_2 = document.createElement("select");
            let delimiter_labels = null;
            if (this.parameter_options[option].type === "date") {
                delimiter_labels = ["At", "Before", "After"];
            }
            else if (this.parameter_options[option].type === "boolean") {
                delimiter_labels = ["true", "false"];
            }
            else { // number
                delimiter_labels = ["Equal_To", "Lower_Than", "Higher_Than"];
            }
            delimiter_labels.forEach(delimiter => {
                let temp_option_element = document.createElement("option");
                temp_option_element.value = delimiter;
                temp_option_element.innerText = delimiter;
                parameter_select_2.appendChild(temp_option_element);
            });
            if (this.parameter_options[option].type === "boolean") {
                parameter_select_2.name = option;
            }
            else {
                parameter_select_2.name = option + "-delimiter";
            }
            // parameter_select_2.value = this.date_delimiters[option];
            // parameter_select_2.onchange = () => {this.active_parameters[input_element.name].delimiter = parameter_select_2.value}
            if (this.parameter_options[option].type === "boolean") {
                parameter_select_2.onchange = () => {this.active_parameters[parameter_select_2.name].value = parameter_select_2.value}
                this.active_parameters[parameter_select_2.name] = {value: parameter_select_2.value, delimiter: null}
            }
            else {
                parameter_select_2.onchange = () => {this.active_parameters[input_element.name].delimiter = parameter_select_2.value}
                this.active_parameters[input_element.name] = {value: input_element.value, delimiter: parameter_select_2.value}
            }
            parameter_select.insertAdjacentElement("afterend", parameter_select_2);
        }
        else { // type is string
            input_element = document.createElement("input");
            input_element.classList.add("ParameterSearchBox");
            input_element.type = "text";
            input_element.onchange = () => {
                this.active_parameters[input_element.name].value = input_element.value;
                // this.doSearch();
            };
        }
        if (this.parameter_options[option].type !== "boolean") {
            input_element.name = option;
            input_element.value = value;
        }
        parameter_select.value = option;
        // if (value) {
        // }
        // else if (this.parameter_options !== {}) {
            // When "add parameter" button is clicked it always sets the constraint to column 1. maybe change this
        //     input_element.name = Object.keys(this.parameter_options)[0];
        // }
        if (this.parameter_options[option].type === "date" || this.parameter_options[option].type === "number") {
            this.active_parameters[option] = {value: value, delimiter: parameter_select_2.value}
        }
        else if (this.parameter_options[option].type === "string") { // We don't want to override the boolean
            this.active_parameters[option] = {value: value, delimiter: null}
        }
        if (this.parameter_options[option].type !== "boolean") {
            parameter_container.appendChild(input_element);
        }

        let delete_button = document.createElement("button");
        delete_button.classList.add("DeleteParameterButton")
        delete_button.innerText = "Delete";
        if (this.parameter_options[option].type === "boolean") {
            delete_button.onclick = (event) => {
                this.parameter_container_container.removeChild(parameter_container);
                delete this.active_parameters[parameter_select_2.name];
                --this.number_of_parameters;
            }
        }
        else {
            delete_button.onclick = (event) => {
                this.parameter_container_container.removeChild(parameter_container);
                delete this.active_parameters[input_element.name];
                --this.number_of_parameters;
            }
        }
        parameter_select.onchange = (event) => {
            let new_value = parameter_select.value;
            let new_type = this.parameter_options[new_value].type;
            // if (this.parameter_options[parameter_select.value].type === "date") {
            //     input_element.type = "date";
            // }
            delete this.active_parameters[option]; // "change" active parameter by deleting the old one
            option = new_value;
            if (this.parameter_options[new_value].type !== "boolean") { // boolean type doesn't have input_element
                if (!parameter_container.contains(input_element)) {
                    input_element = document.createElement("input");
                    parameter_select.insertAdjacentElement("afterend", input_element);
                    input_element.onchange = () => {
                        this.active_parameters[input_element.name].value = input_element.value;
                        // this.doSearch();
                    };
                    console.log("there was no input element i hope");
                }
                input_element.type = new_type;
                input_element.name = new_value;
            }
            else { // Assuming we're switching to boolean
                if (input_element && parameter_container.contains(input_element)) {
                    parameter_container.removeChild(input_element);
                }
                console.log("removing input element?");
            }
            if (new_type === "date" || new_type === "number" || new_type === "boolean") {
                if (parameter_container.contains(parameter_select_2)) {
                    parameter_container.removeChild(parameter_select_2);
                }
                parameter_select_2 = document.createElement("select");
                // parameter_select_2.name = "date_delimiter";
                let delimiter_labels = null;
                if (new_type === "date") {
                    delimiter_labels = ["At", "Before", "After"];
                }
                else if (new_type === "boolean") {
                    delimiter_labels = ["true", "false"];
                }
                else {
                    delimiter_labels = ["Equal_To", "Lower_Than", "Higher_Than"];
                }
                delimiter_labels.forEach(delimiter => {
                    let temp_option_element = document.createElement("option");
                    temp_option_element.value = delimiter;
                    temp_option_element.innerText = delimiter;
                    parameter_select_2.appendChild(temp_option_element);
                });
                if (this.parameter_options[option].type === "boolean") {
                    parameter_select_2.name = new_value;
                }
                else {
                    parameter_select_2.name = new_value + "-delimiter";
                }
                if (new_type === "boolean") {
                    parameter_select_2.onchange = () => {this.active_parameters[new_value].value = parameter_select_2.value}
                    this.active_parameters[new_value] = {value: parameter_select_2.value, delimiter: null}
                }
                else {
                    parameter_select_2.onchange = () => {this.active_parameters[new_value].delimiter = parameter_select_2.value}
                    this.active_parameters[new_value] = {value: input_element.value, delimiter: parameter_select_2.value}
                }
                parameter_select.insertAdjacentElement("afterend", parameter_select_2);
            }
            else { // Assuming we're switching to "string" search type
                // remove the select element
                if (parameter_container.contains(parameter_select_2)) {
                    parameter_container.removeChild(parameter_select_2);
                }
                if (!parameter_container.contains(input_element)) {
                    input_element = document.createElement("input");
                    parameter_select.insertAdjacentElement("afterend", input_element);
                    input_element.onchange = () => {
                        this.active_parameters[input_element.name].value = input_element.value;
                        // this.doSearch();
                    };
                }
                this.active_parameters[new_value] = {value: input_element.value, delimiter: null};
                // this.active_parameters[new_value] = null;
            }
        }
        parameter_container.appendChild(delete_button);

        this.parameter_container_container.appendChild(parameter_container);
        ++this.number_of_parameters;
        // this.search_button.disabled = false;

        // this.container_element.appendChild(fragment);
        // this.parameter_elements.append(parameter_container);
    }

    doSearch() {
        this.json = this.initial_json;
        for (let [parameter, value] of Object.entries(this.active_parameters)) {
            if (this.parameter_options[parameter].type === "string") {
                this.json = this.json.filter(json_row => {
                    return json_row[parameter].toLowerCase().includes(value.value.toLowerCase());
                });
            }
            else if (this.parameter_options[parameter].type === "boolean") {
                this.json = this.json.filter(json_row => {
                    if (json_row[parameter] === true) {
                        return value.value === "true";
                    }
                    else {
                        return value.value === "false";
                    }
                    // return json_row[parameter] == value.value;
                });
            }
            else if (this.parameter_options[parameter].type === "date" || this.parameter_options[parameter].type === "number") {
                if (value.delimiter === "At" || value.delimiter === "Equal_To") {
                    this.json = this.json.filter(json_row => {
                        return json_row[parameter] == value.value;
                    });
                }
                else if (value.delimiter === "Before" || value.delimiter === "Lower_Than") {
                    this.json = this.json.filter(json_row => {
                        return json_row[parameter] < value.value;
                    });
                }
                else { // After
                    this.json = this.json.filter(json_row => {
                        return json_row[parameter] > value.value;
                    });
                }
                console.log(`Search column ${parameter} for ${value.delimiter} ${value.value}`);
            }
        }

        this.setPage(1);
    }
}
*/