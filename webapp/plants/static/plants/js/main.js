const imageInput = document.getElementById("image_input");
const preimg = document.getElementById("display_image");
const imgbutton = document.getElementById("imgbutton");

// set submit button to disable.
imgbutton.disabled = true

// add function to file upload when change
imageInput.addEventListener("change", () => {
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
});


