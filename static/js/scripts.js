// function sendMessage() {
//     var userInput = document.getElementById('chat-input').value;
//     var chatContainer = document.getElementById('chat-messages');

//     // Add user message to the chat container
//     // chatContainer.innerHTML += '<div>User : ' + userInput + '</div>';
//     chatContainer.innerHTML += `
//     <div class="message user-message">
//     <img src="static/icons/user.png" alt="user icon"> <span>${userInput}</span>
//     </div>`;
//     // Send user input to the server
//     fetch('/get_response', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//         },
//         body: 'user_input=' + userInput,
//     })
//     .then(response => response.text())
//     .then(data => {
//         // Add bot's response to the chat container
//         chatContainer.innerHTML += `<div class="message bot-message">
//         <img src="static/icons/chatbot.png" alt="bot icon"> <span>${data}</span>
//         </div>`;
//     });

//     // Clear the user input field
//     document.getElementById('chat-input').value = '';
// }

function sendMessage() {
    var userInput = document.getElementById('chat-input').value;
    var chatContainer = document.getElementById('chat-messages');

    // Add user message to the chat container
    // chatContainer.innerHTML += '<div>User : ' + userInput + '</div>';
    chatContainer.innerHTML += `
    <div class="message user-message">
    <img src="static/icons/user.png" alt="user icon"> <span>${userInput}</span>
    </div>`;
    // Send user input to the server
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user_input=' + userInput,
    })
    .then(response => {
        if (response.headers.get('content-type').includes('image')) {
            return response.blob();
        } else {
            return response.text();
        }
    })
    .then(data =>{
        if (data instanceof Blob) {
            // If the response is an image, create a URL for the blob and display the image
            const imageUrl = URL.createObjectURL(data);
            // chatContainer.innerHTML += `<div class="message bot-message">
            // </div>`;
            chatContainer.innerHTML += `<div class="message bot-message">
                <img src="static/icons/chatbot.png" alt="bot icon">
                <img src="${imageUrl}" alt="bot image" style="width: 600px; height: 450px;"> 
            </div>`;
        } else {
            // If the response is not an image, display the text
            chatContainer.innerHTML += `<div class="message bot-message">
                <img src="static/icons/chatbot.png" alt="bot icon"> <span>${data}</span>
            </div>`;
        }
    })
    // Clear the user input field
    document.getElementById('chat-input').value = '';
}
function deleteRow(id) {
    swal({
        title: "Are you sure?",
        text: "Once deleted, you will not be able to recover this User",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    }).then((result) => {
        if(result){
            //ทำการลบ
            fetch('delete',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: id })
            })
            .then(response => response.json())
            .then(data => {
                //ประมวลผลข้อมูลที่ได้จากเซิร์ฟเวอร์ (ถ้ามี)
                console.log(data.message);
                swal("You delete Completed!", {
                    icon: "success",
                }).then((result) => {
                    if(result){
                        location.reload();
                    }
                })
            })

            .catch(error => {
                console.error('เกิดข้อผิดพลาดในการส่งคำร้อง AJAX:', error);
            })
        }
    })
}

function menuToggle(){
    const toggleMenu = document.querySelector('.menu');
    toggleMenu.classList.toggle('active')
}