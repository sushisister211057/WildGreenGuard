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

    // console.log(imageInput.files[0]);
};






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

