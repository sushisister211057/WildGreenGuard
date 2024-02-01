// const imageInput = document.getElementById("image_input");
// const preimg = document.getElementById("display_image");
// const imgbutton = document.getElementById("imgbutton");
// const uploadBtn = document.getElementById("upload_button");

// set submit button to disable.
// if (imgbutton){
//     imgbutton.disabled = true
// }


function uploadtrigger(){
    const imageInput = document.getElementById("image_input");
    imageInput.click();
};

function showImg(){
    const imageInput = document.getElementById("image_input");
    const preimg = document.getElementById("display_image");
    const imgbutton = document.getElementById("imgbutton");
    const reader = new FileReader();
    
    reader.addEventListener("load", () => {
        preimg.src = reader.result;
    });

    if (imageInput.files[0]) {
        reader.readAsDataURL(imageInput.files[0]);
        imgbutton.disabled = false;
    } else {
        imgbutton.disabled = true;
    }

    console.log(imageInput.files[0]);
};

function Auth() {
    let URL = 'https://access.line.me/oauth2/v2.1/authorize?';
    URL += 'response_type=code';
    URL += '&client_id=';  //請換成你自己的 client_id
    URL += secret;  //請換成你自己的 client_id
    URL += '&redirect_uri='; //請換成你自己的 callback url
    URL += endpoint; //請換成你自己的 callback url
    URL += '&scope=profile%20openid%20email';
    URL += '&state=123453sdfgfd';
    console.log("test")
    //導引到LineLogin
    window.location.href = URL;
    // console.log(test)
}



// imageInput.addEventListener("change", () => {
//     const reader = new FileReader();
    
//     reader.addEventListener("load", () => {
//         preimg.src = reader.result;
//     });

//     if (imageInput.files[0]) {
//         reader.readAsDataURL(imageInput.files[0]);
//         imgbutton.disabled = false;
//     } else {
//         imgbutton.disabled = true;
//     }

//     console.log(imageInput.files[0]);
// });


// add function to trigger file input
// uploadBtn.addEventListener("click", ()=>{
//     console.log("test");
//     imageInput.click();
// })

// document.querySelector("upload_button")

// function triggerFileInput() {
//     // const imageInput = document.getElementById("image_input");
//     console.log("test")
//     imageInput.click();
// }

// add function to file upload when change

