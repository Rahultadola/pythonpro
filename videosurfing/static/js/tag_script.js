import { add_content } from './add_post.js';

let counter = 1;
let start = 1;
let end =0 ;
var page_name_value = page_value;

var string_to_send = '';


const quant = 7;

document.addEventListener('DOMContentLoaded', initiaload);
    
function initiaload(){
    var tag_dict = heading;
    var tag_string = JSON.parse(tag_dict.replace(/&#39;/g, '"'));
    
    //console.log(page_name_value);

    string_to_send = tag_string[0].name;
    make_request();
};

function make_request(){

    start = counter;  
    end = start + quant;
    counter = end + 1;

    const request = new XMLHttpRequest();
    request.open('POST','/yahi_chahiye', true);

    const retData = new FormData();
    retData.append('start' , start);
    retData.append('end' , end);
    retData.append('tag_string' , string_to_send);
    retData.append('page_value' , page_name_value);
   
    request.send(retData);

    request.onload = () => {
      const data = JSON.parse(request.responseText);
      const head_data = data[data.length - 1];
      data.pop()     
      //console.log(data)
      
      if(data[0].dura_time){
        add_content(data, head_data)
      }
               
    };
    

};

window.onscroll = ()=> {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight)
        make_request();
};
