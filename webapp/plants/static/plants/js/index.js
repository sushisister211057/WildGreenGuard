const imageInput = document.getElementById("image_input");
const preimg = document.getElementById("display_image")

imageInput.addEventListener("change", ()=>{
    const reader = new FileReader();
    reader.addEventListener("load", ()=>{
        preimg.src = reader.result;
    });
    if (imageInput.files[0]){
        reader.readAsDataURL(imageInput.files[0])
    }
    console.log(imageInput.files[0])
});
