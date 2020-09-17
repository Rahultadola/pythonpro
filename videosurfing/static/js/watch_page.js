import { add_content } from './add_post.js';


let counter = 1;
let start = 1;
let end =0 ;

let string_to_send = '';

const quant = 7;

var tag_dict = video_tag;
var tag_string = JSON.parse(tag_dict.replace(/&#39;/g, '"'));

var vid = document.getElementById("player");
vid.onplay = () => {
    

    for (var i = tag_string.length - 1; i >= 0; i--) {
        string_to_send += tag_string[i].id; 
    }
    
    make_request();

};



function make_request(){
    start = counter;  
    end = start + quant;
    counter = end + 1;

    const request = new XMLHttpRequest();
    request.open('POST','/related');

    const retData = new FormData();
    retData.append('start' , start);
    retData.append('end' , end);
    retData.append('tag_string' , string_to_send);
   
    request.send(retData);

    request.onload = () => {
      const data = JSON.parse(request.responseText);
            
      if(data[0].dura_time){
        add_content(data)
      }
               
    };
    

};


window.onscroll = ()=> {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight)
        make_request();
};
