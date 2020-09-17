import { add_content } from './add_post.js';

let counter = 1;
let start = 1;
let end = 0 ;

const quant = 7;
var headingDict = heading;
var parsedHeadin = JSON.parse(headingDict.replace(/&#39;/g, '"'));
var flag = 0;

document.addEventListener('DOMContentLoaded', initLoad);

function initLoad() {
    
    start = counter;  
    end = start + quant;
    counter = end + 1;
    
    //console.log(parsedHeadin);
    for(var head of parsedHeadin){ 
      if(flag < 2){
        makeRequest(head);
        ++flag;
      }
    }
};


function makeRequest(head){
    const request = new XMLHttpRequest();
    request.open('POST','/posts', true);

    const retData = new FormData();
    retData.append('start', start);
    retData.append('end', end);
    retData.append('heading', head.name);
    request.send(retData);

    request.onload = () => {
      const data = JSON.parse(request.responseText);
      const headData = data[data.length - 1];
      data.pop()
      //console.log(headData)
      //console.log(data)
      if(data[0].dura_time){
        add_content(data, headData)
    }
               
  };
};
    

window.onscroll = ()=> {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight){
    if(flag < parsedHeadin.length)
    makeRequest(parsedHeadin[flag++]);
  }
};
