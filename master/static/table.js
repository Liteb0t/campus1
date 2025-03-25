class Table {
    constructor(container_id, options = {}) {
        Object.assign(this, {
            page: 1
            ,json: []
            ,json_url: null
            ,columns: {} // name, type, parent_object[]
			,editable: false
        }, options);
		// Generating HTML
        this.container_element = document.getElementById(container_id);
		this.container_element.classList.add("AwesomeTableContainer");
		// this.editable && this.container_element.classList.add("EditableTable");
        // this.advanced_search_container_element = document.createElement("div");
        this.toolbar_element = document.createElement("div");
        this.table_box_element = document.createElement("div");
		this.table_box_element.classList.add("TableBox");
        this.table_element = document.createElement("table");
        this.thead_element = document.createElement("thead");
        this.tbody_element = document.createElement("tbody");

		// Shows current page and what rows are being displayed
		this.showing_indexes_element = document.createElement("div");
		this.showing_indexes_element.textContent = "Loading...";
		this.container_element.appendChild(this.showing_indexes_element);

        let header_row_element = document.createElement("tr");
        for (let column_name of Object.keys(this.columns)) {
			// Add column headers
            let column_element = document.createElement("th");
            column_element.innerText = column_name;
            header_row_element.appendChild(column_element);

			// If a column is not explicitly set to be uneditable, the default is true
			if (this.columns[column_name].type === "array") {
				this.columns[column_name].editable = false;
			}
			else if (typeof this.columns[column_name].editable === "undefined") {
				this.columns[column_name].editable = true;
			}
        }
		if (this.editable) {
            let column_element = document.createElement("th");
            column_element.innerText = "Actions";
			column_element.setAttribute("colspan", 2);
            header_row_element.appendChild(column_element);
		}
        this.thead_element.appendChild(header_row_element);

        this.table_element.appendChild(this.thead_element);
        this.table_element.appendChild(this.tbody_element);
        // this.container_element.appendChild(this.advanced_search_container_element);
        this.container_element.appendChild(this.toolbar_element);
		this.table_box_element.appendChild(this.table_element);
        this.container_element.appendChild(this.table_box_element);

        // Add pagination buttons to the toolbar
        this.first_page_button = document.createElement("button");
        this.first_page_button.textContent = "First";
        this.first_page_button.onclick = () => {this.setPage(1)};
        this.previous_page_button = document.createElement("button");
        this.previous_page_button.textContent = "Previous";
        this.previous_page_button.onclick = () => {this.setPage(this.page - 1)};
        this.next_page_button = document.createElement("button");
        this.next_page_button.textContent = "Next";
        this.next_page_button.onclick = () => {this.setPage(this.page + 1)};
        this.last_page_button = document.createElement("button");
        this.last_page_button.textContent = "Last";
        this.last_page_button.onclick = () => {this.setPage(Math.ceil(this.json.length / entries_per_page))};
        this.updatePageButtons();
        this.toolbar_element.appendChild(this.first_page_button);
        this.toolbar_element.appendChild(this.previous_page_button);
        this.toolbar_element.appendChild(this.next_page_button);
        this.toolbar_element.appendChild(this.last_page_button);

		// More toolbar buttons
		if (this.editable) {
			this.delete_button = document.createElement("button");
			this.delete_button.classList.add("TableDeleteButton");
			this.delete_button.textContent = "Delete selected";
			this.delete_button.disabled = true;
			this.delete_button.onclick = () => {this.deleteRows();}
			this.toolbar_element.appendChild(this.delete_button);
		}

		this.refresh_button = document.createElement("button");
		this.refresh_button.classList.add("TableRefreshButton");
		this.refresh_button.textContent = "Refresh";
		this.refresh_button.onclick = () => {this.refresh();}
		this.toolbar_element.appendChild(this.refresh_button);

		if (this.editable) {
			this.entries_to_delete = {};
		}

        if (this.json.length === 0 && this.json_url !== null) {
            this.refresh();
        }
        else {
            this.populate();
        }
    }
	async processRowForm(row_element, action, json_row) {
		console.log(json_row);
		console.log(row_element);
		let form_data = {
			_id: json_row.id,
			_action: action
		}
		let column_i = 0;
		for (let [column_name, column_attributes] of Object.entries(this.columns)) {
			if (column_attributes.editable) {
				let base_for_entry = form_data;
				if (typeof column_attributes.parent_object !== "undefined") {
					for (let parent_object of column_attributes.parent_object) {
						if (typeof form_data[parent_object] === "undefined") {
							form_data[parent_object] = {};
						}
						base_for_entry = form_data[parent_object];
					}
				}
				console.log(row_element.children[column_i].children[0].value);
				if (column_attributes.type === "boolean") {
					base_for_entry[column_attributes.name] = row_element.children[column_i].children[0].checked;
				}
				else {
					base_for_entry[column_attributes.name] = row_element.children[column_i].children[0].value;
				}
			}
			else {
				let base_for_entry = form_data;
				if (typeof column_attributes.parent_object !== "undefined") {
					for (let parent_object of column_attributes.parent_object) {
						if (typeof form_data[parent_object] === "undefined") {
							form_data[parent_object] = {};
						}
						base_for_entry = form_data[parent_object];
					}
				}
				base_for_entry[column_attributes.name] = json_row[column_attributes.name];
			}
			++column_i;
		}
		console.log(form_data);
		await this.postJSON(this.json_url, form_data);
		this.refresh();
	}
	async deleteRows() {
		let form_data = {
			_action: "deleteMultiple",
			to_delete: Object.keys(this.entries_to_delete)
		};
		await this.postJSON(this.json_url, form_data);
		this.entries_to_delete = [];
		this.refresh();
	}

    populate() {
        // Delete existing rows if there are any
        while (this.tbody_element.lastChild) {
            this.tbody_element.removeChild(this.tbody_element.lastChild);
        }
        let start_index = (this.page - 1) * entries_per_page;
        let until_index = this.page * entries_per_page;

		let showing_indexes_string = ["Page "]; // Its like a stringbuilder
		showing_indexes_string.push(this.page.toString());
		showing_indexes_string.push(" | Showing ");

        if ((this.page - 1) * entries_per_page >= this.json.length) {
			if (this.json.length === 0) {
	            this.tbody_element.textContent = "No data found.";
			}
			else {
				this.tbody_element.textContent = "No data on this page.";
			}
			showing_indexes_string.push("nothing");
        }
        else {
            for (let i = start_index; i < until_index && i < this.json.length; i++) {
                let json_row = this.json[i];
				if (typeof json_row === "undefined") {
					console.log(`Undefined JSON at row ${i}`);
				}
                let table_row_element = document.createElement("tr");
				table_row_element.id = this.container_element.id + "_row_" + i.toString();
                for (let [column_name, column_attributes] of Object.entries(this.columns)) {
                    let cell_element = document.createElement("td");
					if (column_attributes.type === "array") {
						cell_element.textContent = "[" + json_row[column_attributes.name].length + " entries]";
					}
					else {
						cell_element.textContent = this.getNestedValueIfNested(json_row, column_name);
					}
                    table_row_element.appendChild(cell_element);
                }
				if (this.editable) {
					// Add HTML for edit and delete columns
					let edit_entry_td = document.createElement("td");
					let delete_entry_td = document.createElement("td");
					let edit_entry_button = document.createElement("button");
					let confirm_edit_entry_button = document.createElement("button");
					let cancel_edit_entry_button = document.createElement("button");
					let delete_entry_checkbox = document.createElement("input");

					edit_entry_td.classList.add("TableActionColumn1");
					delete_entry_td.classList.add("TableActionColumn2");
					delete_entry_checkbox.type = "checkbox";
					edit_entry_button.classList.add("EntryEditButton");
					confirm_edit_entry_button.classList.add("EntryConfirmEditButton");
					cancel_edit_entry_button.classList.add("EntryCancelEditButton");
					delete_entry_checkbox.classList.add("EntryDeleteCheckbox");
					edit_entry_button.title = "Edit";
					confirm_edit_entry_button.title = "Confirm";
					cancel_edit_entry_button.title = "Cancel";

					confirm_edit_entry_button.style["display"] = "none";
					cancel_edit_entry_button.style["display"] = "none";

					edit_entry_button.onclick = () => {
						console.log(table_row_element.id);
						let column_i = 0;
						for (let [column_name, column_attributes] of Object.entries(this.columns)) {
							if (column_attributes.editable) {
								let cell_input_element = document.createElement("input");
								if (column_attributes.type === "boolean") {
									cell_input_element.type = "checkbox";
									cell_input_element.checked = this.getNestedValueIfNested(json_row, column_name);
								}
								else {
									cell_input_element.type = column_attributes.type;
									cell_input_element.value = this.getNestedValueIfNested(json_row, column_name);
								}
								table_row_element.children[column_i].textContent = "";
								table_row_element.children[column_i].appendChild(cell_input_element);
							}
							++column_i;
						}
						edit_entry_button.style["display"] = "none";
						delete_entry_checkbox.style["display"] = "none";
						confirm_edit_entry_button.style["display"] = "block";
						cancel_edit_entry_button.style["display"] = "block";
					}
					confirm_edit_entry_button.onclick = () => {
						this.processRowForm(table_row_element, "update", json_row);
					};
					cancel_edit_entry_button.onclick = () => {
						let column_i = 0;
						for (let [column_name, column_attributes] of Object.entries(this.columns)) {
							// table_row_element.children[i].removeChild(table_row_element.children[i][0]);
							table_row_element.children[column_i].innerHTML = this.getNestedValueIfNested(json_row, column_name);
							++column_i;
						}
						edit_entry_button.style["display"] = "block";
						delete_entry_checkbox.style["display"] = "block";
						confirm_edit_entry_button.style["display"] = "none";
						cancel_edit_entry_button.style["display"] = "none";
					}
					delete_entry_checkbox.onchange = () => {
						if (delete_entry_checkbox.checked) {
							this.entries_to_delete[json_row.id] = null;
							this.delete_button.disabled = false;
						}
						else {
							delete this.entries_to_delete[json_row.id];
							if (Object.keys(this.entries_to_delete).length === 0) {
								this.delete_button.disabled = true;
							}
						}
					}
					delete_entry_checkbox.checked = typeof this.entries_to_delete[json_row.id] !== "undefined";

					edit_entry_td.appendChild(edit_entry_button);
					edit_entry_td.appendChild(confirm_edit_entry_button);
					// delete_entry_td.appendChild(delete_entry_button);
					delete_entry_td.appendChild(delete_entry_checkbox);
					delete_entry_td.appendChild(cancel_edit_entry_button);
					table_row_element.appendChild(edit_entry_td);
					table_row_element.appendChild(delete_entry_td);
				}
                this.tbody_element.appendChild(table_row_element);
                // table_row_element.onclick = () => {
                //     console.log(`Username: be like ${json_row.username}`);
                // }
            }
			showing_indexes_string.push((start_index+1).toString());
			showing_indexes_string.push("-");
			showing_indexes_string.push(Math.min(until_index, this.json.length).toString());
			showing_indexes_string.push(" of ");
			showing_indexes_string.push(this.json.length.toString());
			this.showing_indexes_element.textContent = showing_indexes_string.join("");
        }
        this.updatePageButtons();
    }
    setPage(page) {
        this.page = page;
        this.populate();
    }
	// "grey out" buttons to prevent paginating outside the bounds of the data
    updatePageButtons() {
        this.first_page_button.disabled = this.page === 1;
        this.previous_page_button.disabled = this.page === 1;
        this.next_page_button.disabled = this.page * entries_per_page >= this.json.length;
		this.last_page_button.disabled = this.next_page_button.disabled && this.page * entries_per_page < this.json.length + entries_per_page || this.json.length === 0;
    }
	// Sometimes a value is nested
	// eg. the "username" attribute is under "sser" which is itself under a "Student"
	getNestedValueIfNested(json_row, column_id) {
		let temp_json_value;
		if (typeof this.columns[column_id].parent_object !== "undefined") {
			temp_json_value = json_row;
			for (let parent_key of this.columns[column_id].parent_object ) {
				temp_json_value = temp_json_value[parent_key];	
			}
			temp_json_value = temp_json_value[this.columns[column_id].name];
		}
		else {
			temp_json_value = json_row[this.columns[column_id].name];
		}
		return temp_json_value;
	}
    async refresh() {
        this.tbody_element.textContent = "Fetching data...";
        const response = await fetch(this.json_url);
        console.log(response);
        if (!response.ok) {
            this.tbody_element.textContent = "There was a problem fetching the data";
        }
        else {
            this.json = await response.json();
			if (this.editable) {
				this.entries_to_delete = [];
				this.delete_button.disabled = true;
			}
            this.populate();
			if (students_table.constructor.name === "AdvancedSearchTable") {
				this.initial_json = this.json;
			}
        }
    }
	// sends JSON to the server. the form handling is in our views.py
	async postJSON(url, data) {
        const fetch_response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
		console.log(fetch_response);
		alert(`ok: ${fetch_response.ok}\nstatus: ${fetch_response.status}\nstatusText: ${fetch_response.statusText}`);
        return fetch_response;
    }
}

class AdvancedSearchTable extends Table {
    constructor(tbody_id, options = {}) {
        super(tbody_id, options);
        // this.advanced_search_container_id = advanced_search_container_id;
        this.linkToHTML();
        this.url_search_params = new URLSearchParams(window.location.search);
        // this.number_of_parameters = 0;
        // this.date_delimiters = {};
        this.active_parameters = {};
        // for (const [parameter_option, properties] of Object.entries(this.columns)) {
        //     if (properties.type === "number") {
        //         console.log("type number");
        //         for (let i = 0; i < this.json.length; i++) {
        //             this.json[i][parameter_option] = Number(this.json[i][parameter_option]);
        //         }
        //     }
        // }
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
        this.advanced_search_container_element = document.createElement("div");
        this.advanced_search_container_element.classList.add("AdvancedSearchContainer");

        this.add_parameter_button = document.createElement("button");
        this.add_parameter_button.classList.add("AddParameterButton");
        this.add_parameter_button.textContent = "Add parameter"
        this.add_parameter_button.type = "button";
        this.add_parameter_button.onclick = () => {
            console.log("Adding a search parameter!");
            this.addSearchParameter();
        };
        this.advanced_search_container_element.appendChild(this.add_parameter_button);

        this.parameter_container_container = document.createElement("div");
        this.parameter_container_container.classList.add("ParameterContainer");
        this.advanced_search_container_element.appendChild(this.parameter_container_container);

        this.search_button = document.createElement("button");
        this.search_button.classList.add("SearchButton");
        // this.search_button.disabled = true;
        this.search_button.textContent = "Search";
        this.search_button.onclick = () => { this.doSearch() };
        this.advanced_search_container_element.appendChild(this.search_button);

		this.container_element.insertAdjacentElement("AfterBegin", this.advanced_search_container_element);
    }

    addSearchParameter(option = null, value = null) {
        // let fragment = new DocumentFragment();
        // When "new parameter" button clicked, it just adds the constraint to the first column
        if (option === null) {
            option = Object.keys(this.columns)[0];
        }

        let parameter_container = document.createElement("div");
        parameter_container.classList.add("SearchParameter");
        // parameter_container.id = `${this.container_id}_${}`
        // fragment.appendChild(parameter_container);

        // Drop down menu of what column to search
        let parameter_select = document.createElement("select");
        for (const [parameter_option, type] of Object.entries(this.columns)) {
            // console.log(`Parameter option: ${parameter_option}`);
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
        if (this.columns[option].type === "date" || this.columns[option].type === "number" || this.columns[option].type === "boolean") {
            if (this.columns[option].type !== "boolean") {
                input_element = document.createElement("input");
                input_element.type = this.columns[option].type;
            }
            // input_element.classList.add("ParameterDateBox");
            parameter_select_2 = document.createElement("select");
            let delimiter_labels = null;
            if (this.columns[option].type === "date") {
                delimiter_labels = ["At", "Before", "After"];
            }
            else if (this.columns[option].type === "boolean") {
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
            if (this.columns[option].type === "boolean") {
                parameter_select_2.name = option;
            }
            else {
                parameter_select_2.name = option + "-delimiter";
            }
            // parameter_select_2.value = this.date_delimiters[option];
            // parameter_select_2.onchange = () => {this.active_parameters[input_element.name].delimiter = parameter_select_2.value}
            if (this.columns[option].type === "boolean") {
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
        if (this.columns[option].type !== "boolean") {
            input_element.name = option;
            input_element.value = value;
        }
        parameter_select.value = option;
        // if (value) {
        // }
        // else if (this.columns !== {}) {
            // When "add parameter" button is clicked it always sets the constraint to column 1. maybe change this
        //     input_element.name = Object.keys(this.columns)[0];
        // }
        if (this.columns[option].type === "date" || this.columns[option].type === "number") {
            this.active_parameters[option] = {value: value, delimiter: parameter_select_2.value}
        }
        else if (this.columns[option].type === "string") { // We don't want to override the boolean
            this.active_parameters[option] = {value: value, delimiter: null}
        }
        if (this.columns[option].type !== "boolean") {
            parameter_container.appendChild(input_element);
        }

        let delete_button = document.createElement("button");
        delete_button.classList.add("DeleteParameterButton")
        delete_button.innerText = "Delete";
		// for booleans there is no input_element, but rather parameter_select_2 stores the column name
        if (this.columns[option].type === "boolean") {
            delete_button.onclick = (event) => {
                this.parameter_container_container.removeChild(parameter_container);
				console.log(parameter_select_2.name);
                delete this.active_parameters[parameter_select_2.name];
                // --this.number_of_parameters;
            }
        }
        else {
            delete_button.onclick = (event) => {
                this.parameter_container_container.removeChild(parameter_container);
                delete this.active_parameters[input_element.name];
                // --this.number_of_parameters;
            }
        }
        parameter_select.onchange = (event) => {
            let new_value = parameter_select.value;
            let new_type = this.columns[new_value].type;
            // if (this.columns[parameter_select.value].type === "date") {
            //     input_element.type = "date";
            // }
            delete this.active_parameters[option]; // "change" active parameter by deleting the old one
            option = new_value;
            if (this.columns[new_value].type !== "boolean") { // boolean type doesn't have input_element
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
                if (this.columns[option].type === "boolean") {
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
			// Update delete button functions
			if (new_type === "boolean") {
        	    delete_button.onclick = (event) => {
        	        this.parameter_container_container.removeChild(parameter_container);
					console.log(parameter_select_2.name);
        	        delete this.active_parameters[parameter_select_2.name];
        	        // --this.number_of_parameters;
        	    }
        	}
        	else {
        	    delete_button.onclick = (event) => {
        	        this.parameter_container_container.removeChild(parameter_container);
        	        delete this.active_parameters[input_element.name];
        	        // --this.number_of_parameters;
        	    }
        	}
        }
        parameter_container.appendChild(delete_button);

        this.parameter_container_container.appendChild(parameter_container);
        // ++this.number_of_parameters;
        // this.search_button.disabled = false;

        // this.container_element.appendChild(fragment);
        // this.parameter_elements.append(parameter_container);
    }

    doSearch() {
        this.json = this.initial_json;
        for (let [parameter, value] of Object.entries(this.active_parameters)) {
            if (this.columns[parameter].type === "string") {
                this.json = this.json.filter(json_row => {
                    return this.getNestedValueIfNested(json_row, parameter).toLowerCase().includes(value.value.toLowerCase());
                });
            }
            else if (this.columns[parameter].type === "boolean") {
                this.json = this.json.filter(json_row => {
                    return this.getNestedValueIfNested(json_row, parameter) === (this.active_parameters[parameter].value === "true");
                });
            }
            else if (this.columns[parameter].type === "date" || this.columns[parameter].type === "number") {
                if (value.delimiter === "At" || value.delimiter === "Equal_To") {
                    this.json = this.json.filter(json_row => {
                        return this.getNestedValueIfNested(json_row, parameter) == value.value;
                    });
                }
                else if (value.delimiter === "Before" || value.delimiter === "Lower_Than") {
                    this.json = this.json.filter(json_row => {
                        return tthis.getNestedValueIfNested(json_row, parameter) < value.value;
                    });
                }
                else { // After
                    this.json = this.json.filter(json_row => {
                        return tthis.getNestedValueIfNested(json_row, parameter) > value.value;
                    });
                }
                console.log(`Search column ${parameter} for ${value.delimiter} ${value.value}`);
            }
        }

        this.setPage(1);
    }
}

