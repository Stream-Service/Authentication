document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.getElementById("loginBtn");

  loginBtn.addEventListener("click", async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      // Prepare form data
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      // Step 1: Login request
      const loginResponse = await fetch("http://127.0.0.1:8009/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
        credentials: "include"
      });

      


      if (loginResponse.status === 403) {
        const error = await loginResponse.json();
        document.getElementById("status").innerText = `❌ Login failed: ${error.detail}`;
        return;
      }

      if (!loginResponse.ok) {
        document.getElementById("status").innerText = `❌ Unexpected error: ${loginResponse.statusText}`;
        return;
      }

      // Parse tokens
      const data = await loginResponse.json();
      localStorage.setItem("accessToken", data.access_token);
      localStorage.setItem("refreshToken", data.refresh_token);
      




      document.getElementById("status").innerText = "✅ Login successful!";

      console.log("Login response status:", loginResponse.status);
      
      // console.log("Login data:", data);
      // const token2 = data.access_token;
      // console.log("Token:", token2);
 



      // Step 2: Call /users/profile with Bearer token
       
      const profileResponse = await fetch("http://127.0.0.1:8009/users/profile", {
        method: "GET",
        headers: {
    "Authorization": `Bearer ${data.access_token}`,   // 🔑 add token here
    "Content-Type": "application/json"    // optional, but good practice
  },
        credentials: "include"
      });
      console.log("Profile response status:", profileResponse.status);
      if (profileResponse.ok) {
        // If backend returns HTML, replace page
        const html = await profileResponse.text();
        document.open();
        document.write(html);
        document.close();
      } else {
        document.getElementById("status").innerText = "❌ Failed to load profile page";
        console.error("Profile error:", profileResponse.status, profileResponse.statusText);
      }

    } catch (err) {
      document.getElementById("status").innerText = `❌ Network error: ${err}`;
    }
  });

  document.getElementById("menuToggle").addEventListener("click", function() {
  document.getElementById("navLinks").classList.toggle("show");
});

// Active link highlight
const navItems = document.querySelectorAll(".nav-item");
navItems.forEach(item => {
  item.addEventListener("mouseover", () => {
    item.style.transform = "scale(1.05)";
  });
  item.addEventListener("mouseout", () => {
    item.style.transform = "scale(1)";
  });
});
});


