function getErrors(errors_json, out, reverse_accessor_path) {
	console.log(reverse_accessor_path);
	console.log(errors_json);
	for (let [key, value] of Object.entries(errors_json)) {
		if (key === "message") {
			continue;
		}
		else if (key == "errors") {
			getErrors(value, out, reverse_accessor_path);
		}
		else if (Object.prototype.toString.call(value) === "[object Array]") {
			console.log("cvalue is arraw");
			out.push({name: key, parameter: reverse_accessor_path[key], errors: value});
		}
		else if (typeof value === "object") {
			console.log("cvalue is NOT arraw");
			console.log(key);
			// parent_objects.push(key);
			getErrors(value, out, reverse_accessor_path[key]);
		}
	}
}
function showErrors(processed_errors, parameters_object) {
	for (let i = 0; i < processed_errors.length; ++i) {
		let error_element = document.createElement("div");
		error_element.textContent = processed_errors[i].errors.join("\n");
		error_element.classList.add("FormError");
		parameters_object[processed_errors[i].parameter].insertAdjacentElement("afterend", error_element);
	}
}
function clearErrors(form_element) {
	for (let error_element of form_element.querySelectorAll(".FormError")) {
		form_element.removeChild(error_element);
	}
}
