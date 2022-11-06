window.onload=()=>{
    const boxElement=document.getElementsByClassName("box");
   
    let boxNum=3;
    let arrayOfFlats=[];
    
    let indexOfchecked=0;

    document.body.innerHTML += '<div class="standart"><div class="text">Эталонный объект</div></div> ';
    for(let i=0;i<boxNum;i++){
       
        document.body.innerHTML += '<div class="box"><label><input type="checkbox"></label></div>';
     
    }
  /*  
*/
}