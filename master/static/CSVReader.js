class CSVReader {
    constructor(input_id) {
        this.input_element = document.getElementById(input_id);
        this.raw_data = "test";
        this.parsed_data = [];
        this.input_element.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                this.parsed_data = [];
                console.log(this.parsed_data);
                let columns = [];
                reader.onload = function(e) {
                    this.parsed_data = [];
                    console.log(this.parsed_data);
                    console.log(this.raw_data);
                    this.raw_data = e.target.result;
                    console.log(this.raw_data);
                    let content_s = this.raw_data.replace("\r\n", "\n").split("\n");
                    if (content_s[content_s.length-1] === "") {
                        content_s.pop();
                    }
                    console.log(content_s);
                    console.log(this.parsed_data);
                    for (let header of content_s[0].split(",")) {
                        columns.push(header.trim());
                    }
                    console.log(columns)
                    for (let i = 1; i < content_s.length; ++i) {
                    console.log(this.parsed_data);
                        let data_s = content_s[i].split(",");
                        let new_row = {};
                        for (let column_i = 0; column_i < columns.length; ++column_i) {
                            new_row[columns[column_i]] = data_s[column_i].trim();
                        }
                        console.log(new_row)
                        console.log(this.parsed_data);
                        this.parsed_data.push(new_row);
                    }
                    // document.getElementById('output').innerText = content;
                    console.log(this.parsed_data);
                };
                reader.readAsText(file);
            }
        });
    }
}
