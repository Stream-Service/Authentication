 document.addEventListener("DOMContentLoaded", () => {
    const uuu = getCookie("user_id");
    const toc = getCookie("access_token");
    console.log("aaqqq",uuu)

    const videobutton = document.getElementById("startUploadVideoBtn");
    videobutton.addEventListener("click",(e)=>{

       

      
        uploadVideo();

      
    });

    const postbutton = document.getElementById("startUploadPostBtn");
    postbutton.addEventListener("click",(e)=>{

      console.log('ededhgjh')

       

      
        uploadpost();

      
    });
     
 
     
     
     
  
    
    
    // Open modal
     
     

    // Upload logic
    
    async function uploadVideo() {
      console.log("User__ID:", uuu);
      console.log("Access_Token:", toc);
      const fileInput = document.getElementById("videoInput");
      const title = document.getElementById("videoTitle").value;
      const description = document.getElementById("videoDescription").value;
      const tags = document.getElementById("videoTags").value;
      const status = document.getElementById("videoUploadStatus");
      if (!fileInput.files.length) {
        status.innerText = "Please select a video file.";
        return;
      }

      const file = fileInput.files[0];
      const chunkSize = 2 * 1024 * 1024;
      const videoId = crypto.randomUUID();

      status.innerText = "Uploading...";

      for (let start = 0, index = 0; start < file.size; start += chunkSize, index++) {
        const chunk = file.slice(start, start + chunkSize);
        try {
          const response=await fetch("http://127.0.0.1:8082/upload-chunk", {
            method: "POST",
            headers: {
              "Content-Type": "application/octet-stream",
              "X-Video-ID": videoId,
              "X-Chunk-Index": index.toString(),
              "Authorization": `Bearer ${toc}`

            },
            credentials: "include",
             
            body: chunk
          });

          if (response.status === 401) {
      // Redirect to login page window.location.href = "/login";
      return; // stop uploading further chunks
    }
          if (!response.ok) {
      status.innerText = `Error uploading chunk ${index + 1}: ${response.statusText}`;
      return;
    }

    status.innerText = `Uploaded chunk ${index + 1}`;
  } catch (err) {
    status.innerText = `Error uploading chunk ${index + 1}: ${err}`;
    return;
  }
}
      try {
  const response = await fetch("http://127.0.0.1:8082/finalize-upload", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${toc}`
    },
    credentials: "include",
    body: JSON.stringify({
      user_id:uuu,
      video_id: videoId,
      title:title,
      description:description,
       
    })
  });

  // 🔍 Check if token is invalid
  if (response.status === 401) {
    // Redirect to login page
    window.location.href = "/login";
    return;
  }

  if (!response.ok) {
    status.innerText = `❌ Error finalizing upload: ${response.statusText}`;
    return;
  }

  status.innerText = "✅ Upload complete and finalized!";
} catch (err) {
  status.innerText = `❌ Network error during finalize: ${err}`;
}

        try {
  const response = await fetch("http://127.0.0.1:8010/add_video_metadata", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${toc}`   // 🔑 include token
    },
    body: JSON.stringify({
      user_id:userId,
      video_id: videoId,
      title:title,
      description:description,
      video_url: "https://cdn.example.com/videos/abc123.mp4",
      thumbnail: "https://cdn.example.com/thumbnails/abc123.jpg",
      
       
    })
  });

  // 🔍 Check token validity
  if (response.status === 401) {
    window.location.href = "/login";   // redirect to login
    return;
  }

  if (!response.ok) {
    status.innerText = `❌ Metadata save failed: ${response.statusText}`;
    return;
  }

  status.innerText += "\n✅ Metadata saved successfully!";
} catch (err) {
  status.innerText = `❌ Finalization or metadata save failed: ${err}`;
}}



async function uploadpost() {
  console.log("User__ID:", uuu);
  console.log("Access_Token:", toc);

  const fileInput = document.getElementById("postInput");
  const title = document.getElementById("postTitle").value;
  const description = document.getElementById("postDescription").value;
  const poststatus = document.getElementById("postUploadStatus");

  if (!fileInput.files.length) {
    poststatus.innerText = "Please select an image file.";
    return;
  }

  const imgfile = fileInput.files[0];
  poststatus.innerText = "Uploading...";

  try {
    // ✅ Use FormData
    const formData = new FormData();
    formData.append("user_id", uuu);        // must match Form(...)
    formData.append("title", title);        // must match Form(...)
    formData.append("content", description);// must match Form(...)
    formData.append("image", imgfile);      // must match File(...)

    const response = await fetch("http://127.0.0.1:8010/posts", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${toc}` // ✅ don't set Content-Type, browser will handle it
      },
      credentials: "include",
      body: formData
    });

    if (response.status === 401) {
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      poststatus.innerText = `❌ Error: ${response.statusText}`;
      return;
    }

    const data = await response.json();
    poststatus.innerText = "✅ Post uploaded successfully!";
    console.log("Response:", data);
  } catch (err) {
    poststatus.innerText = `❌ Network error: ${err}`;
  }
}


    });
