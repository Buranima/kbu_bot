var kbu_bot_socket = io();
var data = {};
var id = null;

function fetchData() {
    // ส่งคำขอข้อมูลจากฐานข้อมูล โดยกำหนด mode เป็น "read" เพื่อดึงข้อมูล
    var data_form_database_json = { mode: "DATABASE-READ" };
    kbu_bot_socket.emit("DATA-BASE", data_form_database_json);
}

// Listen for the data from the server
kbu_bot_socket.on("DATA-BASE", (on_data_form_database_json) => {
    data = JSON.parse(on_data_form_database_json["result"]);
    // console.log(data); // Debugging output

    // ล้างข้อมูลใน DataTable เดิม
    var table = $('#myTable').DataTable();
    table.clear();

    // // เติมข้อมูลลงในตาราง DataTable
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

// เรียกใช้งาน fetchData() ทุกๆ 30 วินาที (30000 milliseconds)
setInterval(fetchData, 100000);

// เรียก fetchData ครั้งแรกเมื่อโหลดหน้าเพจ
fetchData();


// จัดการคลิกปุ่มแก้ไขข้อมูล
$(document).on('click', '.editBtn', function() {
    id = Number($(this).attr('id')); 
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
    // รับค่าจากฟิลด์ input
    var Question = $('#questionInput').val().trim();
    var Answer = $('#answerInput').val().trim();

    // ตรวจสอบว่าค่าที่กรอกไม่เป็นค่าว่าง
    if (!Question || !Answer) {
        alert("กรุณากรอกข้อมูลคำถามและคำตอบให้ครบถ้วน");
        return;
    }
    // แสดงโมเดลยืนยันการบันทึกข้อมูล
    $('#confirmSaveModal').modal('show');
});

// จัดการเมื่อคลิกปุ่มยืนยันการบันทึก
$('#confirmSave').on('click', function() {
    id = Number($('#recordId').val());
    var updatedQuestion = $('#questionInput').val();
    var updatedAnswer = $('#answerInput').val();

    var data_form_database_json = {
        mode: "DATABASE-UP-DATE",
        id: id,
        question: updatedQuestion,
        answer: updatedAnswer
    };
    kbu_bot_socket.emit("DATA-BASE", data_form_database_json);

    $('#confirmSaveModal').modal('hide');
    $('#editModal').modal('hide');
    showLoading();

    // รอการตอบกลับเพื่อลบหน้าจอโหลด
    kbu_bot_socket.once("DATA-BASE", function(response) {
    hideLoading(); // ซ่อนหน้าจอโหลด
    // console.log(response); // แสดงข้อความตอบกลับ
    });

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
$('#saveAdd').on('click', function() {;
    // รับค่าจากฟิลด์ input
    var newQuestion = $('#questionInputNew').val().trim();
    var newAnswer = $('#answerInputNew').val().trim();

    // ตรวจสอบว่าค่าที่กรอกไม่เป็นค่าว่าง
    if (!newQuestion || !newAnswer) {
        alert("กรุณากรอกข้อมูลคำถามและคำตอบให้ครบถ้วน");
        return;
    }

    // แสดงโมเดลยืนยันการบันทึกข้อมูล
    $('#confirmSaveModalAdd').modal('show');
});

$('#confirmSaveAdd').on('click', function() {
    var newQuestion = $('#questionInputNew').val();
    var isDuplicate = false;
    var duplicateId = null;
    var duplicateAnswer = null;

    // ตรวจสอบว่า data และ data.question ถูกกำหนดแล้ว
    if (data && data.question && data.question.length > 0) {
        // ตรวจสอบว่ามีคำถามซ้ำกันในข้อมูลที่มีอยู่หรือไม่
        for (let i = 0; i < data.question.length; i++) {
            if (data.question[i] === newQuestion) {
                isDuplicate = true;
                duplicateId = data.id[i]; // เก็บ id ของข้อมูลที่ซ้ำกัน
                duplicateAnswer = data.answer[i]; // เก็บคำตอบที่ซ้ำกันด้วย
                break;
            }
        }
    }

    if (isDuplicate) {
        // ถ้าพบว่าข้อมูลซ้ำกัน ให้แสดง editModal แทน
        $('#questionInput').val(newQuestion);
        $('#answerInput').val(duplicateAnswer); // ใส่คำตอบที่ซ้ำกันเพื่อให้แก้ไขได้
        $('#recordId').val(duplicateId);

        $('#addModal').modal('hide');
        $('#editModal').modal('show');
        $('#confirmSaveModalAdd').modal('hide');
    } else {
        // ถ้าไม่พบข้อมูลซ้ำ ให้ดำเนินการเพิ่มข้อมูลใหม่
        var data_form_database_json = {
            mode: "DATABASE-INSERT",
            question: newQuestion,
            answer: $('#answerInputNew').val()
        };
        
        // ส่งข้อมูลใหม่ไปยังเซิร์ฟเวอร์เพื่อทำการเพิ่ม
        kbu_bot_socket.emit("DATA-BASE", data_form_database_json);

        // ปิดโมเดลหลังจากเพิ่มข้อมูลใหม่
        $('#confirmSaveModalAdd').modal('hide');
        $('#addModal').modal('hide');
        showLoading();

        // รอการตอบกลับเพื่อลบหน้าจอโหลด
        kbu_bot_socket.once("DATA-BASE", function(response) {
        hideLoading(); // ซ่อนหน้าจอโหลด
        // console.log(response); // แสดงข้อความตอบกลับ
        });
    }
});



// // คลิกปุ่ม "ยืนยันการเพิ่มข้อมูล"
// $('#confirmSaveAdd').on('click', function() {
//     var newQuestion = $('#questionInputNew').val();
//     var newAnswer = $('#answerInputNew').val();

//     var data_form_database_json = {
//         mode: "insert",
//         question: newQuestion,
//         answer: newAnswer
//     };
    
//     // ส่งข้อมูลใหม่ไปยังเซิร์ฟเวอร์เพื่อทำการเพิ่ม
//     kbu_bot_socket.emit("data-form-database", data_form_database_json);

//     // ปิดโมเดลหลังจากเพิ่มข้อมูลใหม่
//     $('#confirmSaveModalAdd').modal('hide');
//     $('#addModal').modal('hide');
// });




// จัดการคลิกปุ่มลบข้อมูล
$(document).on('click', '.deleteBtn', function() {
    // แสดงโมเดลยืนยันการลบข้อมูล
    id = Number($(this).attr('id'));
    $('#confirmDeleteModal').modal('show');
});

// เมื่อยืนยันการลบ
$('#confirmDelete').on('click', function() {
    var data_form_database_json = {
        mode: "DATABASE-DELETE",
        id: id
    };
    // ส่งคำขอไปยังเซิร์ฟเวอร์เพื่อลบข้อมูล
    kbu_bot_socket.emit("DATA-BASE", data_form_database_json);

    // ปิดโมเดลยืนยันการลบ
    $('#confirmDeleteModal').modal('hide');
    showLoading();

    // รอการตอบกลับเพื่อลบหน้าจอโหลด
    kbu_bot_socket.once("DATA-BASE", function(response) {
    hideLoading(); // ซ่อนหน้าจอโหลด
    // console.log(response); // แสดงข้อความตอบกลับ
    });
});

function showLoading() {
    $('#loadingModal').modal('show');
}

function hideLoading() {
    $('#loadingModal').modal('hide');
}