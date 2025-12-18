function copyToClipboard(elementId, button) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text).then(() => {
      button.innerText = "✅ Copied!";
      setTimeout(() => {
        button.innerText = button.id === "accessBtn" ? "📋 Copy Access Token" : "📋 Copy Refresh Token";
      }, 2000);
    });
  }
function parseJwt(token) {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
}

document.getElementById("uploadLink").addEventListener("click", async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("accessToken");
  console.log(token)
  const response = await fetch("/upload", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (response.ok) {
    const html = await response.text();
    document.open();
    document.write(html);
    document.close();
  } else {
    alert("Unauthorized");
  }
});





document.getElementById("video").addEventListener("click", async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("accessToken");
  console.log(token)
  const response = await fetch("/videos", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (response.ok) {
    const html = await response.text();
    document.open();
    document.write(html);
    document.close();
  } else {
    alert("Unauthorized");
  }
});

function openPopup(url) {
  document.getElementById("popupFrame").src = url;
  document.getElementById("popupModal").style.display = "block";
}

document.getElementById("closeBtn").onclick = function() {
  document.getElementById("popupModal").style.display = "none";
};

