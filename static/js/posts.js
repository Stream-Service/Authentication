const posts_grid = document.getElementById("Container");

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

const user_id = getCookie("user_id"); // matches your HTML id

async function load_posts(user_id) {
  try {
    const response_posts = await fetch(`http://127.0.0.1:8010/posts/User/${user_id}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    if (!response_posts.ok) throw new Error("Failed to fetch posts");

    const posts = await response_posts.json();

    // Clear old posts
    posts_grid.innerHTML = "";

    for (const p of posts) {
      const div_post = document.createElement("div");
      div_post.className = "post";

      

       
            
         

      // Thumbnail
      const thumbnail_div = document.createElement("div");
      thumbnail_div.className = "thumbnail_section";
      const img = document.createElement("img");

      try {
        const res = await fetch(`http://127.0.0.1:8006/posts?user_id=${p.user_id}&post_id=${p.post_id}`);
        const data = await res.json();
        img.src = data.url || "";
      } catch (err) {
        console.error("Error fetching presigned URL:", err);
      }

      img.className = "thumbnail";
      thumbnail_div.appendChild(img);

      // Description
      const description_div = document.createElement("div");
      description_div.className = "description_section";
      description_div.innerHTML = `
        <h3>${p.post.title}</h3>
        <p>${p.post.content}</p>
        <span>Views: ${p.post.views}</span>
      `;

      // Buttons
      const button_div = document.createElement("div");
      button_div.className = "button_section";
      button_div.innerHTML = `
        <button class="likeBtn">👍 Like ${p.likes}</button>
        <button class="dislikeBtn">👎 Dislike ${p.dislikes}</button>
      `;

      // Post header with options
      const post_header = document.createElement("div");
      post_header.className = "post_header";

      const user_div = document.createElement("div");
      user_div.className = "user-info";
      user_div.innerHTML = `
  <img src="http://127.0.0.1:8010/profile-pic/${p.user_id}" 
       alt="err" 
       class="user-pic"
       onclick="openPopup('/pop/${p.user_id}')">
  <span class="username">Hritik</span>
`;

      const optionsBtn = document.createElement("button");
      optionsBtn.className = "optionsBtn";
      optionsBtn.textContent = "⋮";

      const dropdown = document.createElement("div");
      dropdown.className = "dropdown";
      dropdown.innerHTML = `
        <ul>
          <li class="deleteOption">🗑️ Delete</li>
        </ul>
      `;
      dropdown.style.display = "none";

      // Toggle dropdown
      optionsBtn.onclick = (e) => {
        e.stopPropagation(); // prevent bubbling
        dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
      };

      // Delete handler
      dropdown.querySelector(".deleteOption").onclick = async () => {
        if (confirm("Are you sure you want to delete this post?")) {
          try {
            const res = await fetch(`http://127.0.0.1:8010/posts/${p.post.post_id}`, {
              method: "DELETE",
              headers: { "Content-Type": "application/json" }
            });
            if (!res.ok) throw new Error("Failed to delete post");
            div_post.remove(); // remove from UI
          } catch (err) {
            alert("Error deleting post");
          }
        }
      };
      post_header.appendChild(user_div);
      post_header.appendChild(optionsBtn);
      post_header.appendChild(dropdown);
      div_post.appendChild(post_header);

      div_post.appendChild(thumbnail_div);
      div_post.appendChild(description_div);
      div_post.appendChild(button_div);

      posts_grid.appendChild(div_post);

      // Like/Dislike event listeners
      const likeBtn = button_div.querySelector(".likeBtn");
      likeBtn.textContent = `👍 Like ${p.post.likes}`;
      likeBtn.onclick = () => handleLike(p.post.post_id, likeBtn);

      const dislikeBtn = button_div.querySelector(".dislikeBtn");
      dislikeBtn.textContent = `👎 Dislike ${p.post.dislikes}`;
      dislikeBtn.onclick = () => handleDislike(p.post.post_id, dislikeBtn);

      // Close dropdown if clicking outside
      document.addEventListener("click", (event) => {
        if (!post_header.contains(event.target)) {
          dropdown.style.display = "none";
        }
      });
    }
  } catch (err) {
    alert("Error n : " + err);
  }
}

// Handlers
async function handleLike(postId, likeBtn) {
  try {
    const res_like = await fetch(`http://127.0.0.1:8010/posts/like/${postId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    if (!res_like.ok) throw new Error("Failed to add likes");
    await res_like.json();
  } catch (err) {
    alert("Try again");
  }
  let currentCount = parseInt(likeBtn.textContent.replace(/\D/g, "")) || 0;
  currentCount++;
  likeBtn.textContent = `👍 Like ${currentCount}`;
}

async function handleDislike(postId, dislikeBtn) {
  try {
    const res_dislike = await fetch(`http://127.0.0.1:8010/posts/dislike/${postId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    if (!res_dislike.ok) throw new Error("Failed to add dislikes");
    await res_dislike.json();
  } catch (err) {
    alert("Try again");
  }
  let currentCount = parseInt(dislikeBtn.textContent.replace(/\D/g, "")) || 0;
  currentCount++;
  dislikeBtn.textContent = `👎 Dislike ${currentCount}`;
}

async function handleDislike(postId, dislikeBtn) {
  try {
    const res_dislike = await fetch(`http://127.0.0.1:8010/posts/dislike/${postId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    if (!res_dislike.ok) throw new Error("Failed to add dislikes");
    await res_dislike.json();
  } catch (err) {
    alert("Try again");
  }
  let currentCount = parseInt(dislikeBtn.textContent.replace(/\D/g, "")) || 0;
  currentCount++;
  dislikeBtn.textContent = `👎 Dislike ${currentCount}`;
}


function openPopup(url) {
  document.getElementById("popupFrame").src = url;
  document.getElementById("popupModal").style.display = "block";
}

document.getElementById("closeBtn").onclick = function() {
  document.getElementById("popupModal").style.display = "none";
};
// ✅ Run automatically when page loads
document.addEventListener("DOMContentLoaded", () => {
  load_posts(user_id);
});
