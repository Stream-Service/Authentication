 


 

const token = localStorage.getItem("accessToken");
const payload = parseJwt(token);
 
const left = document.getElementById('left'); 
const gallery = document.getElementById('gallery'); 
  
  
   
 

// const modal = document.getElementById("vp");

const modal = document.getElementById("videoModal");
const closeBtn = document.getElementById("closePopup");
const videoPlayer = document.getElementById("videoPlayer");
const commentsContainer = document.getElementById("commentsContainer");
const likeBtn = document.getElementById("likeBtn");
const dislikeBtn = document.getElementById("dislikeBtn");
const subsbutton= document.getElementById("Subscribe");
const likeCountEl = document.getElementById("likeCount");
const dislikeCountEl = document.getElementById("dislikeCount");
const submitCommentBtn = document.getElementById("submitComment");
const newCommentInput = document.getElementById("newComment");

const USER_ID = 5;
let CURRENT_VIDEO_ID = null;

// Fetch all videos from API and render list
async function loadVideoList(user_id) {
  try {
    const response = await fetch(`http://127.0.0.1:8010/api/videos?user_id=${user_id}&page=0&limit=10`);
    if (!response.ok) throw new Error("Failed to fetch videos");
    const videos = await response.json();

    const videoList = document.getElementById("videoList");
    videoList.innerHTML = "";
     
    videos.forEach(v => {

        const div_card= document.createElement("div");
        div_card.className = "video-card";

// Header with title + menu dots
        const header = document.createElement("div");
        header.className = "card-header";
        header.innerHTML = `
         
        <span class="menu-dots">⋮</span>`;

        const menu = document.createElement("div");
        menu.className = "dropdown-menu";
        menu.innerHTML = `
        <ul>
            <li>Edit</li>
            <li>Delete</li>
            <li>Share</li>
        </ul>
        `;
        menu.style.display = "none"; // hidden by default
        header.appendChild(menu);

        header.querySelector(".menu-dots").onclick = (e) => {e.stopPropagation(); // prevent card click
  menu.style.display = menu.style.display === "none" ? "block" : "none";
};

// Thumbnail
        const img = document.createElement("img");
        img.src = v.thumbnail_url;
        img.alt = v.title;
        img.className = "thumbnail";

// Description section
        const description_div = document.createElement("div");
        description_div.className = "description_section";
        
         
        
      const span_div1 = document.createElement("span");
      span_div1.innerText= v.title
      const span_div = document.createElement("span");
      span_div.innerText= v.views
      const user_div = document.createElement("div");
      user_div.className = "user-info";
       
      user_div.innerHTML = `
  <img src="http://127.0.0.1:8009/users/${v.user_id}/profile-pic" 
       alt="err" 
       class="user-pic"
       onclick="openPopup('/pop/${v.user_id}')">
  <span class="username">Hritik</span>
`;

// Build card
        div_card.appendChild(header);
        div_card.appendChild(img);
        description_div.appendChild(span_div1)
        description_div.appendChild(span_div)
        
        description_div.appendChild(user_div) 
        div_card.appendChild(description_div);

        img.onclick = () => openVideo(v.video_id, v.manifest_url);
        videoList.appendChild(div_card);
        

       
    });
    gallery.appendChild(videoList);
    left.appendChild(gallery);
  } catch (err) {
    console.error("❌ Error loading video list:", err);
  }
}

// Open modal for a specific video
 
async function openVideo(videoId, videoUrl) {
  CURRENT_VIDEO_ID = videoId;
  modal.style.display = 'flex';
  videoPlayer.pause();
  videoPlayer.src = '';

  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(videoUrl);
    hls.attachMedia(videoPlayer);
  } else if (videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
    videoPlayer.src = videoUrl; // Safari fallback
  }

  videoPlayer.play(); // may require muted
  await loadComments(CURRENT_VIDEO_ID);
}
// Close modal
closeBtn.onclick = () => { modal.style.display = "none"; };
window.onclick = (event) => { if (event.target === modal) modal.style.display = "none"; };

// Load comments
async function loadComments(video_id) {
  commentsContainer.innerHTML = "Loading comments...";
  try {
    const response = await fetch(`http://127.0.0.1:8010/videos/comments/${video_id}`);
    if (!response.ok) throw new Error("Failed to fetch comments");
    const comments = await response.json();

    commentsContainer.innerHTML = "";
    comments.forEach(c => {
      const date = new Date(c.created_at).toLocaleString();
      const div = document.createElement("div");
      div.className = "comment";
      div.innerHTML = `
        <strong>${c.user.id}</strong> 
        <span style="color:gray;font-size:12px;">(${date})</span>
        <p>${c.content}</p>
      `;
      commentsContainer.appendChild(div);
    });
  } catch (err) {
    commentsContainer.innerHTML = `❌ Error loading comments: ${err}`;
  }
}

// Load stats
 

// Like/Dislike
async function handleLike(USER_ID,video_id) {
  try {
    const response = await fetch(`http://127.0.0.1:8010/videos/like/${video_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: USER_ID })
    });
    if (!response.ok) throw new Error("Failed to like video");
    const result = await response.json();
    likeCountEl.innerText = result.likes;
  } catch (err) {
    alert(`❌ Error: ${err}`);
  }
}

async function handleDislike(user_id,video_id){
  try {
    const response = await fetch(`http://127.0.0.1:8010/videos/dislike/${video_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: user_id })
    });
    if (!response.ok) throw new Error("Failed to dislike video");
    const result = await response.json();
    dislikeCountEl.innerText = result.dislikes;
  } catch (err) {
    alert(`❌ Error: ${err}`);
  }
}



 // Add comment
async function addComment(user_id,video_id) {
  const content = newCommentInput.value.trim();
  if (!content) {
    alert("Please enter a comment");
    return;
  }
  try {
    const response = await fetch(`http://127.0.0.1:8010/videos/comment/${video_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: user_id,
        video_id: video_id,
        content: content
      })
    });

    if (!response.ok) throw new Error("Failed to add comment");

    // Clear input
    newCommentInput.value = "";

    // Reload comments to show the new one
    await loadComments(CURRENT_VIDEO_ID);
  } catch (err) {
    alert(`❌ Error adding comment: ${err}`);
  }
}




async function Subscribe(follower_id,following_id) {
   
  try {
    const response = await fetch(`http://127.0.0.1:8003/follow`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        follower_id:follower_id,
        following_id:following_id,
         
      })
    });

    if (!response.ok) throw new Error("Failed to follow");

    // Clear input
    newCommentInput.value = "";

    // Reload comments to show the new one
    await loadComments(CURRENT_VIDEO_ID);
  } catch (err) {
    alert(`❌ Error adding comment: ${err}`);
  }
}

/// Bind events (make sure they are functions, not immediate calls)
likeBtn.onclick = () => handleLike(USER_ID,CURRENT_VIDEO_ID);
dislikeBtn.onclick = () => handleDislike(USER_ID,CURRENT_VIDEO_ID);
submitCommentBtn.onclick = () => addComment(USER_ID, CURRENT_VIDEO_ID);
subsbutton.onclick = () => Subscribe(USER_ID, USER_ID);


// Load video list automatically on page load
document.addEventListener("DOMContentLoaded", () => {
  loadVideoList(USER_ID);
});

 
