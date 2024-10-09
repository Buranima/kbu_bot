var kbu_bot_socket = io();

    // Listen for the data from the server
    kbu_bot_socket.on("data-form-database", (on_data_form_database_json) => {
        const data = JSON.parse(on_data_form_database_json);
        console.log(data); // Debugging output

        // Clear the DataTable
        var table = $('#myTable').DataTable();
        table.clear();

        // Populate the table with the new data
        for (let i = 0; i < data.id.length; i++) {
            const question = data.question[i];
            const answer = data.answer[i];
            table.row.add([
                question,
                answer,
                `<button type="button" id=data.id class="btn btn-primary btn-sm">แก้ไขข้อมูล</button>
                 <button type="button" id=data.id class="btn btn-danger btn-sm">ลบข้อมูล</button>`
            ]);
        }

        // Draw the DataTable
        table.draw();
    });

    // Emit the request for data
    var data_form_database_json = { mode: "read" };
    kbu_bot_socket.emit("data-form-database", data_form_database_json);
