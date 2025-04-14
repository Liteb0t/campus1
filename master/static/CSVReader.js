class CSVReader {
    constructor(container_id, upload_url) {
		this.container_element = document.getElementById(container_id);
        this.input_element = this.container_element.querySelector("input");
        this.raw_data = "test";
        this.parsed_data = [];
		let success_indicator_element = document.createElement("div");
		this.container_element.appendChild(success_indicator_element);

        this.input_element.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                // this.parsed_data = [];
                let columns = [];
                reader.onload = async function(e) {
					let successful_uploads = 0;
					let failed_uploads = 0;
                    this.parsed_data = [];
                    this.raw_data = e.target.result;
                    console.log(this.raw_data);
                    let content_s = this.raw_data.replace("\r\n", "\n").split("\n");
                    if (content_s[content_s.length-1] === "") {
                        content_s.pop();
                    }
                    console.log(content_s);
                    for (let header of content_s[0].split(",")) {
                        columns.push(header.trim());
                    }
                    console.log(columns)
                    for (let i = 1; i < content_s.length; ++i) {
                        let data_s = content_s[i].split(",");
                        let new_row = {};
                        for (let column_i = 0; column_i < columns.length; ++column_i) {
                            new_row[columns[column_i]] = data_s[column_i].trim();
                        }
                        console.log(new_row)
                        this.parsed_data.push(new_row);
                    }
                    // document.getElementById('output').innerText = content;
                    console.log(this.parsed_data);
					// this.uploadData(this.parsed_data);
					for (let csv_row of this.parsed_data) {
						// let first_name = csv_row
						let data = {};
						let first_name = csv_row["Attached To"].substring(0, csv_row["Attached To"].indexOf(" "));
						let last_name = csv_row["Attached To"].substring(csv_row["Attached To"].indexOf(" ")+1, csv_row["Attached To"].length);
						console.log(first_name);
						console.log(last_name);
						data = {
							"_action": "create",
							"user": {
								"first_name": first_name,
								"last_name": last_name,
								"username": csv_row["Student Number"],
								"email": csv_row["Student Number"] + "@hallam.shu.ac.uk",
								"password": makeRandomPassword(32)  // Students will set their passwords thru their emails
							},
							"on_visa": csv_row["Attatched To Tier 4"] === "TRUE",
							"eligible_to_work": csv_row["Eligible to work"] === "TRUE",
							"hours_worked": 0
							// "hours_worked": 0
						};
						let response = Form.postJSON(upload_url, data);
						response.then(value => {
							console.log(value.status);
							if (value.status === 200 || value.status === 201) {
								++successful_uploads;
							}
							else {
								++failed_uploads;
							}
							success_indicator_element.textContent = `Succeeded: ${successful_uploads}, Failed: ${failed_uploads}`;
							if (successful_uploads + failed_uploads === this.parsed_data.length) {
								success_indicator_element.textContent = success_indicator_element.textContent + "\nFinished.";
							}
						});
						// let response_json = await response.json();
					}
                };
                reader.readAsText(file);
            }
        });
    }
	uploadData(parsed_csv) {
		for (let csv_row of parsed_csv) {
			// let first_name = csv_row
			let data = {};
			let first_name = csv_row["Attatched To"].substring(0, csv_row["Attatched To"].indexOf(" "));
			let last_name = csv_row["Attatched To"].substring(csv_row["Attatched To"].indexOf(" ")+1, csv_row["Attatched To"].length-1);
			console.log(last_name);
		}
	}

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

	// Students will set their passwords thru their emails
	// https://stackoverflow.com/a/1349426
	function makeRandomPassword(length) {
		let result = '';
		const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@$%^&*';
		const charactersLength = characters.length;
		let counter = 0;
		while (counter < length) {
		  result += characters.charAt(Math.floor(Math.random() * charactersLength));
		  counter += 1;
		}
		return result;
	}
}
