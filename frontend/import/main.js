window.onload=()=>{
    const uploadFile=document.getElementById("upload-file");
   // const uploadImp=document.getElementById("import-btn");
    const uploadBtn=document.getElementById("import-btn");
    const uploadText=document.getElementById("upload-text");

    uploadBtn.addEventListener("click",function(){
    uploadFile.click();

    });
    let uploded=true;
    let podpis="Файл не загружен";
    uploadFile.addEventListener("change",function(){
if(uploadFile.value){
    uploadText.innerText=uploadFile.value.match(/[\/\\]([\w\d\s\.\-(\)]+)$/)[1];
}

else {
    uploadText.innerText=podpis;
    uploded=false;
}
console.log(uploded);
    });

}
