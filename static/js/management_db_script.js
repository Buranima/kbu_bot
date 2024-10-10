var kbu_bot_socket = io();

// Listen for the data from the server
kbu_bot_socket.on("data-form-database", (on_data_form_database_json) => {
    const data = JSON.parse(on_data_form_database_json);
    console.log(data); // Debugging output

    // ล้างข้อมูลใน DataTable เดิม
    var table = $('#myTable').DataTable();
    table.clear();

    // เติมข้อมูลใหม่ลงในตาราง DataTable
    for (let i = 0; i < data.id.length; i++) {
        const question = data.question[i];
        const answer = data.answer[i];
        const id = data.id[i];
        table.row.add([
            question,
            answer,
            `<button type="button" id="${id}" class="btn btn-primary btn-sm editBtn">แก้ไขข้อมูล</button>
             <button type="button" id="${id}" class="btn btn-danger btn-sm deleteBtn">ลบข้อมูล</button>`
        ]);
    }

    // วาด DataTable ใหม่หลังจากเพิ่มข้อมูล
    table.draw();
});

// ส่งคำขอข้อมูลจากฐานข้อมูล โดยกำหนด mode เป็น "read" เพื่อดึงข้อมูล
var data_form_database_json = { mode: "read" };
kbu_bot_socket.emit("data-form-database", data_form_database_json);

// จัดการคลิกปุ่มแก้ไขข้อมูล
$(document).on('click', '.editBtn', function() {
    var id = $(this).attr('id'); 
    var row = $(this).closest('tr');
    var question = row.find('td:eq(0)').text(); 
    var answer = row.find('td:eq(1)').text(); 

    // ตั้งค่าคำถามและคำตอบใน input ของโมดัลแก้ไขข้อมูล
    $('#questionInput').val(question);
    $('#answerInput').val(answer);
    $('#recordId').val(id); // เก็บ id ไว้ใน hidden input เพื่อใช้อ้างอิงตอนบันทึก

    // แสดงโมเดลแก้ไขข้อมูล
    $('#editModal').modal('show');
});

// จัดการเมื่อคลิกปุ่มบันทึกการเปลี่ยนแปลง
$('#saveChanges').on('click', function() {
    // แสดงโมเดลยืนยันการบันทึกข้อมูล
    $('#confirmSaveModal').modal('show');
});

// จัดการเมื่อคลิกปุ่มยืนยันการบันทึก
$('#confirmSave').on('click', function() {
    var id = $('#recordId').val();
    var updatedQuestion = $('#questionInput').val();
    var updatedAnswer = $('#answerInput').val();

    var data_form_database_json = {
        mode: "update",
        id: id,
        question: updatedQuestion,
        answer: updatedAnswer
    };
    kbu_bot_socket.emit("data-form-database", data_form_database_json);

    $('#confirmSaveModal').modal('hide');
    $('#editModal').modal('hide');

});


// คลิกปุ่ม "เพิ่มข้อมูลใหม่"
$('#addNewRecord').on('click', function() {
    // รีเซ็ตฟอร์มในโมเดลให้เป็นค่าว่าง
    $('#questionInputNew').val('');
    $('#answerInputNew').val('');

    // แสดงโมเดลเพิ่มข้อมูลใหม่
    $('#addModal').modal('show');
});

// จัดการเมื่อคลิกปุ่มบันทึกการเปลี่ยนแปลง
$('#saveAdd').on('click', function() {
    // แสดงโมเดลยืนยันการบันทึกข้อมูล
    $('#confirmSaveModalAdd').modal('show');
});

// คลิกปุ่ม "ยืนยันการเพิ่มข้อมูล"
$('#confirmSaveAdd').on('click', function() {
    var newQuestion = $('#questionInputNew').val();
    var newAnswer = $('#answerInputNew').val();

    var data_form_database_json = {
        mode: "insert",
        question: newQuestion,
        answer: newAnswer
    };
    
    // ส่งข้อมูลใหม่ไปยังเซิร์ฟเวอร์เพื่อทำการเพิ่ม
    kbu_bot_socket.emit("data-form-database", data_form_database_json);

    // ปิดโมเดลหลังจากเพิ่มข้อมูลใหม่
    $('#confirmSaveModalAdd').modal('hide');
    $('#addModal').modal('hide');
});

// จัดการคลิกปุ่มลบข้อมูล
$(document).on('click', '.deleteBtn', function() {
    var id = $(this).attr('id');

    // แสดงโมเดลยืนยันการลบข้อมูล
    $('#confirmDeleteModal').modal('show');

    // เมื่อยืนยันการลบ
    $('#confirmDelete').on('click', function() {
        var data_form_database_json = {
            mode: "delete",
            id: id
        };
        
        // ส่งคำขอไปยังเซิร์ฟเวอร์เพื่อลบข้อมูล
        kbu_bot_socket.emit("data-form-database", data_form_database_json);

        // ปิดโมเดลยืนยันการลบ
        $('#confirmDeleteModal').modal('hide');
    });
});
