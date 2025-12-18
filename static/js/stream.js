
    
    
//     // Load videos immediately on page load
//     document.addEventListener("DOMContentLoaded", () => {

//     let page = 0;
//     let loading = false;
//     const token4 = localStorage.getItem("accessToken");
//     const left = document.getElementById('left'); 
//     const gallery = document.getElementById('gallery'); 
//     const playerModal = document.getElementById('playerModal'); 
//     const closePlayer = document.getElementById('closePlayer'); 
//     const player = document.getElementById('videoPlayer');
     
//     const token3 = localStorage.getItem("accessToken");
//     console.log("User2 ID:", token3);
//     const payload = parseJwt(token3);
//     const user_id=payload.sub
    
//   loadVideos();
// });
    

//     async function loadVideos() {
//       const userId = getCookie("user_id");
//       console.log("User ID:", userId);
//       const toc = getCookie("access_token");
//       if (loading) return;
//       loading = true;
//       const res = await fetch(`http://127.0.0.1:8010/api/videos/?user_id=${userId}&page=${page}`);
//       const videos = await res.json();
//       console.log(videos)
//       videos.forEach(video => {
//         const card = document.createElement('div');
//         card.className = 'video-card';
//         card.onclick = () => playVideo(video.manifest_url);

//         const img = document.createElement('img');
//         img.src = video.thumbnail_url;

//         const info = document.createElement('div');
//         info.className = 'video-info';
//         info.innerHTML = `
//           <h3>${video.title || 'Untitled Video'}</h3>
//           <p>${video.description || 'No description available.'}</p>
//           <div class="tags">${video.tags || ''}</div>
//         `;

//         card.appendChild(img);
//         card.appendChild(info);
//         gallery.appendChild(card);
//         left.appendChild(gallery)
//       });
//       page++;
//       loading = false;
//     }

//     function playVideo(manifestUrl) {
//       playerModal.style.display = 'flex';
//       player.pause();
//       player.src = '';
//       const hls = new Hls();
       
//       hls.loadSource(manifestUrl);
//       hls.attachMedia(player);
//       player.play();
//     }

//     closePlayer.onclick = () => { playerModal.style.display = 'none'; player.pause(); };
   