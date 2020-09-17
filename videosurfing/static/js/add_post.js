export function add_content( data, heading_value){

    const content = document.createElement('div');
    content.className = 'content'; 

    if(heading_value){
         const heading = document.createElement('div');
         heading.className = 'heading';  

         if(heading_value.heading_img){
             const heading_img = document.createElement('img');
             heading_img.className = 'heading_img';
             heading_img.src = heading_value.heading_img;
             heading.append(heading_img);
         }

         const heading_link = document.createElement('a');
         heading_link.className = 'heading_link';
         if(heading_value.heading_link){
            heading_link.href = heading_value.heading_link;
            }

         const h2 = document.createElement('h2');

         h2.className = 'heading_name';
         if(heading_value.name){
         h2.innerHTML = heading_value.name;
        }
         
         heading_link.append(h2); 
         heading.append(heading_link);
         content.append(heading);
         
         
         if(heading_value.name){const hr = document.createElement('hr');content.append(hr);}
      }

     
     
          
     const clearfix = document.createElement('div');
     clearfix.className = 'clearfix';
     
     for (var singleData of data) {
            
             //console.log(typeof singleData);
        if(singleData.vid_name){
             const responsive = document.createElement('div');
             responsive.className = 'responsive';

             const gallery = document.createElement('div');
             gallery.className = 'gallery'; 

             const post_link = document.createElement('a');
             post_link.className = 'post_link';
             post_link.href = singleData.post_link;

             const post = document.createElement('div');
             post.className = 'post';

             const img_holder = document.createElement('div');
             img_holder.className = 'img_holder';

             const thumb_img = document.createElement('img');
             thumb_img.className = 'thumb_img';
             thumb_img.src = singleData.thumb_img;
             
             thumb_img.id = 'thumb_img';
             //console.log(thumb_img.id);

             const dura_time = document.createElement('div');
             dura_time.className = 'dura_time'; 
             //console.log(singleData.dura_time);
             dura_time.innerHTML = singleData.dura_time;

             const vid_title = document.createElement('div');
             vid_title.className = 'vid_title';
             //console.log(singleData.vid_name);
             vid_title.innerHTML = singleData.vid_name;

             const vid_views = document.createElement('small');
             vid_views.className = 'vid_views';
             //console.log(singleData.views);
             vid_views.innerHTML = singleData.views;

             const vid_info = document.createElement('div');
             vid_info.className = 'vid_info';

            img_holder.append(thumb_img);
            img_holder.append(dura_time); 
            post.append(img_holder);
            vid_info.append(vid_title);
            vid_info.append(vid_views);
            post.append(vid_info);

            if (post != null) {
               post_link.append(post);
            }
            else {
               //console.log("Element is null")
            }

              gallery.appendChild(post_link);
              responsive.append(gallery);
                
              
              clearfix.append(responsive);
            }
        


      }
 content.append(clearfix); 

 const adv = document.createElement('div');
 adv.className = 'adv'; 
 adv.innerHTML = "Place for adv";
 
 document.querySelector('#main').append(content);
 content.append(adv);
// adding new code

}; 
