function uploadtrigger(img){
    const imageInput = document.getElementById(img);
    imageInput.click();
};

function showImg(img, display, btn){
    const imageInput = document.getElementById(img);
    const preimg = document.getElementById(display);
    const imgbutton = document.getElementById(btn);
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
