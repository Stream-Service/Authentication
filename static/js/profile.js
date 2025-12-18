 
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}


function openEditModal() { document.getElementById("editModal").style.display = "flex"; }
function closeEditModal() { document.getElementById("editModal").style.display = "none"; }

function openEditModal2() { document.getElementById("editModal2").style.display = "flex"; }
function closeEditModal2() { document.getElementById("editModal2").style.display = "none"; }

async function submitEditProfile() {
  console.log("User__ID:", userId);
  console.log("Access_Token:", toc);
  const form = document.getElementById("editForm");
  const data = {
  role: form.elements["role"].value || null,
  job: form.elements["job"].value || null,
  about: form.elements["about"].value || null,
  location: form.elements["location"].value || null,
  phone_no: form.elements["phone_no"].value || null
  
};
  console.log("Access_Token:", data);

  const response = await fetch('http://127.0.0.1:8008/users/userinfo', {
  method: "POST",
  headers: {
  "Content-Type": "application/json",
  "Authorization": `Bearer ${toc}`   // use your token variable
},
  body: JSON.stringify(data)
});
  if (!response.ok) { alert("Update failed"); return; }
  alert("Profile updated successfully!"); location.reload();
}
const userId = getCookie("user_id");
const toc = getCookie("access_token");

function openPopup(url) {
  document.getElementById("popupFrame").src = url;
  document.getElementById("popupModal").style.display = "block";
}

document.getElementById("closeBtn").onclick = function() {
  document.getElementById("popupModal").style.display = "none";
};

async function submitEditPic() {
  console.log("User__ID:", userId);
  console.log("Access_Token:", toc);

  const file = document.getElementById("videoInput").files[0];
  const formData = new FormData();
  formData.append("image", file);

  // ✅ Use backticks and correct variable name
  const response = await fetch(`http://127.0.0.1:8010/upload/profile/${userId}`, {
    method: "POST",
    body: formData
  });
  if (!response.ok) { alert("Update failed"); return; }
  alert("Profile picture updated successfully!"); location.reload();
}
 