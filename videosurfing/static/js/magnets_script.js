var headingDict = heading;
var parsedHeadin = JSON.parse(headingDict.replace(/&#39;/g, '"'));
var flag = 0
document.addEventListener('DOMContentLoaded', initLoad);

function initLoad() {
    console.log(parsedHeadin);
    for(var value of parsedHeadin){ 
        add_to_view(value);
    }

    var refr_btn = document.getElementsByClassName("refr");
    for(const button of refr_btn) {
      button.addEventListener('click', makeRequest);
    }
    function makeRequest(){
        var gid = this.parentElement.firstChild.innerHTML;
        console.log(gid)
        const request = new XMLHttpRequest();
        request.open('POST','/dheja_batti/GetMagInfo/', true);
        const retData = new FormData();
        retData.append('gid', gid);
        request.send(retData);

        request.onload = () => {
          const data = JSON.parse(request.responseText);
          console.log(data)
          console.log(data[0].gid)
          if(data[0].gid){
            var gids = document.getElementsByClassName('gid');
            for(gid of gids){
              if(gid.innerHTML == data[0].gid){
                var c = gid.parentElement.childNodes;
                c[2].innerHTML = data[0].downloaded;
              }
            }
          }
          else{
            var alrt = document.createElement('div');
            alrt.className = 'model';
            alrt.innerHTML = 'Data Not Found'
          }
        };
    };


    var add2aria_btn = document.getElementsByClassName("add2aria");
    for(const button of add2aria_btn) {
      button.addEventListener('click', add2ariaRequest);
    }
    function add2ariaRequest(){
        var gid = this.parentElement.firstChild.innerHTML;
        
        const request = new XMLHttpRequest();
        request.open('POST','/dheja_batti/AddMag2Aria/', true);
        const retData = new FormData();
        retData.append('gid', gid);
        request.send(retData);

        request.onload = () => {
          const data = JSON.parse(request.responseText);
          console.log(data)
          console.log(data[0].gid)
          if(data[0].gid){
            var gids = document.getElementsByClassName('gid');
            for(gid of gids){
              if(gid.innerHTML == data[0].gid){
                var c = gid.parentElement.childNodes;
                c[2].innerHTML = data[0].downloaded;
              }
            }
          }
          else{
            var alrt = document.createElement('div');
            alrt.className = 'model';
            alrt.innerHTML = 'Data Not Found'
          }
        };

    };

    

  // working - remove torrent button
  var rfdb_btn = document.getElementsByClassName("removefrmdatabase");
  for(const button of rfdb_btn) {
    button.addEventListener('click', rfdbRequest);
  }
  function rfdbRequest(){
      var gid = this.parentElement.firstChild.innerHTML;
      
      const request = new XMLHttpRequest();
      request.open('POST','/dheja_batti/torrent_remove', true);
      const retData = new FormData();
      retData.append('gid', gid);
      request.send(retData);
      };


  };



function add_to_view(torr){
    if(torr.gid){
        const respons = document.createElement('div');
        respons.className = 'respons';

        const gid = document.createElement('div');
        gid.className = 'gid';
        gid.id = 'gid'; 
        console.log(torr.gid);
        gid.innerHTML = torr.gid;

        const torr_title = document.createElement('div');
        torr_title.className = 'torr_title';
        console.log(torr.title);
        torr_title.innerHTML = torr.title;
             
        const downloaded = document.createElement('div');
        downloaded.className = 'downloaded';
        downloaded.id = 'downloaded';
        //console.log(torr.views);
        if(torr.download=='NotAdded'){
          downloaded.innerHTML='NA '+'<i class="fa fa-retweet" aria-hidden="true"></i>'; 
        }
        else{   downloaded.innerHTML = torr.downloaded;}
         
        const post_link = document.createElement('a');
        post_link.className = 'post_link btn';
        post_link.href = torr.add_video_link;
        post_link.innerHTML = '<i class="fa fa-rocket" aria-hidden="true"></i>';

        const refr = document.createElement('button');
        refr.className = 'refr btn';
        refr.innerHTML = '<i class="fa fa-refresh" aria-hidden="true"></i>';

        const add2aria = document.createElement('button');
        add2aria.className = 'add2aria btn';
        add2aria.id = 'add2aria';
        add2aria.innerHTML = '<i class="fa fa-plus" aria-hidden="true"></i>';

        const removefrmdatabase = document.createElement('button');
        removefrmdatabase.className = 'removefrmdatabase btn';
        removefrmdatabase.id = 'removefrmdatabase';
        removefrmdatabase.innerHTML = '<i class="fa fa-minus" aria-hidden="true"></i>';

        const get_data = document.createElement('button');
        get_data.className = 'get_data btn';
        get_data.id = 'get_data';
        get_data.innerHTML = '<i class="fa fa-star" aria-hidden="true"></i>';

        respons.append(gid);
        respons.append(torr_title); 
        respons.append(downloaded);
        respons.append(post_link);
        respons.append(add2aria);
        respons.append(removefrmdatabase);
        respons.append(refr);
        
        respons.append(get_data);


        var main = document.getElementById('main');
        main.append(respons);
      }
};


