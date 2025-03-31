class Form {
	constructor(container_id, options = {}) {
		Object.assign(this, {
			parameters: {},
			name: "defaultname",
			selected_id: null,
			fetch_url: "",
			post_url: ""
		}, options);
		this.container_element = document.getElementById(container_id);
		this.container_element.classList.add("FormContainer");
		this.topbar_element = document.createElement("div");
		this.topbar_element.classList.add("Topbar");
		this.selected_indicator_element = document.createElement("b");
		this.selected_indicator_element.classList.add("SelectedIndicator");
		this.form_element = document.createElement("div");
		this.form_element.classList.add("Form");

		this.selected_indicator_element.textContent = `No ${this.name} selected.`;
		this.topbar_element.appendChild(this.selected_indicator_element);
		this.container_element.appendChild(this.topbar_element);
		this.first_input_element = null;
		this.reverse_accessor = {};
		console.log(this.parameters);
		for (const [parameter_name, parameter_properties] of Object.entries(this.parameters)) {
			if (typeof parameter_properties.editable !== "undefined" && !parameter_properties.editable && parameter_properties.type !== "array") {
				continue;
			}
			let id_stringbuilder = [this.name];
			if (typeof parameter_properties.parent_object !== "undefined") {
				for (const parent_object of parameter_properties.parent_object) {
					id_stringbuilder.push("__");
					id_stringbuilder.push(parent_object);
				}
			}
			id_stringbuilder.push("_");
			id_stringbuilder.push(parameter_properties.name);
			let input_id = id_stringbuilder.join("");
			if (parameter_properties.type === "array") {
				let fieldset_element = document.createElement("fieldset");
				let legend_element = document.createElement("legend");
				legend_element.textContent = parameter_name;
				fieldset_element.appendChild(legend_element);
				let add_button = document.createElement("button");
				add_button.textContent = "Add";
				add_button.onclick = () => {
					this.addArrayEntry(parameter_name);
				}
				fieldset_element.appendChild(add_button);
				this.parameters[parameter_name]["fieldset_element"] = fieldset_element;
				this.parameters[parameter_name]["add_button"] = add_button;
				this.form_element.appendChild(fieldset_element);
			}
			else {
				let label_element = document.createElement("label");
				label_element.setAttribute("for", input_id);
				label_element.textContent = parameter_name;
				let input_element = document.createElement("input");
				if (parameter_properties.type === "string") {
					input_element.type = "text";
				}
				else if (parameter_properties.type === "boolean") {
					input_element.type = "checkbox";
				}
				else {
					input_element.type = parameter_properties.type;
				}
				input_element.id = input_id;
				input_element.name = input_id;
				if (typeof parameter_properties.default !== "undefined") {
					input_element.value = parameter_properties.default;
				}
				this.form_element.appendChild(label_element);
				this.form_element.appendChild(input_element);
				this.parameters[parameter_name]["input_element"] = input_element;
				if (!this.first_input_element) {
					this.first_input_element = input_element;
				}
			}
			// this.form_element.appendChild(document.createElement("br"));
			let base_for_entry = this.reverse_accessor;
			if (typeof parameter_properties.parent_object !== "undefined") {
				for (let parent_object of parameter_properties.parent_object) {
					if (typeof base_for_entry[parent_object] === "undefined") {
						base_for_entry[parent_object] = {};
					}
					base_for_entry = base_for_entry[parent_object];
				}
			}
			base_for_entry[parameter_properties.name] = parameter_name;
		}
		this.create_button = document.createElement("button");
		this.create_button.onclick = () => { this.submitForm("create") };
		this.create_button.textContent = "Create";
		this.update_button = document.createElement("button");
		this.update_button.onclick = () => { this.submitForm("update") };
		this.update_button.textContent = "Update";
		this.update_button.disabled = true;
		this.deselect_button = document.createElement("button");
		this.deselect_button.onclick = () => { this.deselect() };
		this.deselect_button.textContent = "Deselect";
		this.deselect_button.classList.add("DeselectButton");
		this.deselect_button.disabled = true;
		this.topbar_element.appendChild(this.deselect_button);
		this.container_element.appendChild(this.form_element);
		this.container_element.appendChild(this.create_button);
		this.container_element.appendChild(this.update_button);
		this.last_fetch_response = "test";
	}
	deselect() {
		for (const [parameter_name, parameter_properties] of Object.entries(this.parameters)) {
			if (typeof parameter_properties.editable !== "undefined" && !parameter_properties.editable && parameter_properties.type !== "array") {
				continue;
			}
			if (parameter_properties.type === "array") {
				while (parameter_properties.fieldset_element.firstChild !== parameter_properties.add_button) {
					parameter_properties.fieldset_element.removeChild(parameter_properties.fieldset_element.children[0]);
				}
			}
			else if (parameter_properties.type === "boolean") {
				this.parameters[parameter_name].input_element.checked = false;
			}
			else {
				if (typeof parameter_properties.default !== "undefined") {
					this.parameters[parameter_name].input_element.value = parameter_properties.default;
				}
				else {
					this.parameters[parameter_name].input_element.value = "";
				}
			}
		}
		this.selected_indicator_element.textContent = `No ${this.name} selected.`;
		this.deselect_button.disabled = true;
	}

	addArrayEntry(parameter_name, array_item = null) {
		let array_item_container_element = document.createElement("div");
		array_item_container_element.classList.add("ArrayItem");
		let array_item_input_element = document.createElement("input");
		array_item_input_element.type = "number";
		array_item_input_element.setAttribute("min", 0);
		if (array_item) {
			array_item_input_element.value = array_item.id;
		}
		let array_item_delete_button = document.createElement("button");
		array_item_delete_button.textContent = "delete";
		array_item_delete_button.onclick = () => {
			this.parameters[parameter_name].fieldset_element.removeChild(array_item_container_element);
		}
		array_item_container_element.appendChild(array_item_input_element);
		array_item_container_element.appendChild(array_item_delete_button);
		this.parameters[parameter_name].add_button.insertAdjacentElement("beforebegin", array_item_container_element);
	}
	async selectEntry(entry_id) {
		this.selected_id = entry_id;
		let url = this.fetch_url.replace('0', this.selected_id).replace("placeholdername", this.name);
		this.update_button.disabled = true;
		this.deselect_button.disabled = true;
		this.selected_indicator_element.textContent = `Loading ${this.name}...`;
		let response = await fetch(url);
		await response.json().then(response_obj => {
			console.log(response_obj);
			// this.selected_id = response_obj.id;
			// this.selected_indicator_element.removeChild(this.selected_indicator_element.lastChild);
			this.selected_indicator_element.textContent = `Selected ${this.name}: ${this.selected_id}`;
			this.update_button.disabled = false;
			this.deselect_button.disabled = false;

			// Fill out the form
			for (const [parameter_name, parameter_properties] of Object.entries(this.parameters)) {
				if (typeof parameter_properties.editable !== "undefined" && !parameter_properties.editable && parameter_properties.type !== "array") {
					continue;
				}
				let temp_json_value;
				if (parameter_properties.type === "array") {
					while (parameter_properties.fieldset_element.firstChild !== parameter_properties.add_button) {
						parameter_properties.fieldset_element.removeChild(parameter_properties.fieldset_element.children[0]);
					}
					for (let array_item of response_obj[parameter_properties.name]) {
						this.addArrayEntry(parameter_name, array_item);
					}
				}
				else if (parameter_properties.blank) {
					if (parameter_properties.type === "boolean") {
						this.parameters[parameter_name].input_element.checked = false;
					}
					else {
						this.parameters[parameter_name].input_element.value = "";
					}
				}
				else {
					if (typeof parameter_properties.parent_object !== "undefined") {
						temp_json_value = response_obj;
						for (let parent_key of parameter_properties.parent_object ) {
							temp_json_value = temp_json_value[parent_key];	
						}
						temp_json_value = temp_json_value[parameter_properties.name];
					}
					else {
						temp_json_value = response_obj[parameter_properties.name];
					}
					if (parameter_properties.type === "boolean") {
						this.parameters[parameter_name].input_element.checked = temp_json_value;
					}
					else {
						this.parameters[parameter_name].input_element.value = temp_json_value;
					}
				}
			}
		});
	}
	async submitForm(action) {
		let form_data = {
			_id: this.selected_id,
			_action: action
		}
		for (let [parameter_name, parameter_properties] of Object.entries(this.parameters)) {
			if (parameter_properties.type === "array") {
				let temp_array = [];
				for (let array_entry of parameter_properties.fieldset_element.querySelectorAll(".ArrayItem")) {
					temp_array.push(array_entry.children[0].value);
				}
				form_data[parameter_properties.name] = temp_array;
			}
			else if (typeof parameter_properties.editable !== "undefined" && !parameter_properties.editable) {
				continue;
			}
			else {
				let base_for_entry = form_data;
				if (typeof parameter_properties.parent_object !== "undefined") {
					for (let parent_object of parameter_properties.parent_object) {
						if (typeof form_data[parent_object] === "undefined") {
							form_data[parent_object] = {};
						}
						base_for_entry = form_data[parent_object];
					}
				}
				if (parameter_properties.type === "boolean") {
					base_for_entry[parameter_properties.name] = parameter_properties.input_element.checked;
				}
				else {
					base_for_entry[parameter_properties.name] = parameter_properties.input_element.value;
				}
			}
		}
		console.log(form_data);
		let response = await Form.postJSON(this.post_url, form_data);
		let response_json = await response.json();
		console.log(response);
		this.last_fetch_response = response;
		if (response.status === 201) {
			// success
			this.deselect();
		}
		else if (response.status === 400) { // The form was probably invalid.
			let out = [];
			this.getErrors(response_json, out);
			this.showErrors(out);
			console.log(out);
			alert("the thing failed. damn that sucks");
		}
		else if (response.status === 500) {
			alert("server error. yikes that's rough");
		}
		else {
			alert(`Status: ${response.status} (${response.statusText})\nsomething weird happened`);
		}
		console.log(response_json);
		this.first_input_element.focus();
	}
	// sends JSON to the server. the form handling is in our views.py
	static async postJSON(url, data) {
	    const fetch_response = await fetch(url, {
	        method: "POST",
	        body: JSON.stringify(data),
	        headers: {
	            "Content-type": "application/json; charset=UTF-8"
	        }
	    });
		console.log(fetch_response);
		// const json = await fetch_response.json();
	    // return json;
		return fetch_response;
	}
	getErrors(errors_json, out = [], reverse_accessor_path = this.reverse_accessor) {
		for (let [key, value] of Object.entries(errors_json)) {
			if (Object.prototype.toString.call(value) === "[object Array]") {
				out.push({name: key, parameter: reverse_accessor_path[key], errors: value});
			}
			else if (typeof value === "object") {
				// parent_objects.push(key);
				this.getErrors(value, out, reverse_accessor_path[key]);
			}
			// else {
			// 	out.push({name: key, parent_object: parent_objects});
			// }
		}
	}
	showErrors(processed_errors) {
		for (let error_element of this.form_element.querySelectorAll(".FormError")) {
			this.form_element.removeChild(error_element);
		}
		for (let i = 0; i < processed_errors.length; ++i) {
			let error_element = document.createElement("div");
			error_element.textContent = processed_errors[i].errors.join("\n");
			error_element.classList.add("FormError");
			this.parameters[processed_errors[i].parameter].input_element.insertAdjacentElement("afterend", error_element);
		}
	}

	// getErrors(errors_json, out = [], parent_objects = []) {
	// 	for (let [key, value] of Object.entries(errors_json)) {
	// 		if (Object.prototype.toString.call(value) === "[object Array]") {
	// 			out.push({name: key, errors: value, parent_object: parent_objects});
	// 		}
	// 		else if (typeof value === "object") {
	// 			// parent_objects.push(key);
	// 			this.getErrors(value, out, [ ...parent_objects, key]);
	// 		}
	// 		// else {
	// 		// 	out.push({name: key, parent_object: parent_objects});
	// 		// }
	// 	}
	// }
}
