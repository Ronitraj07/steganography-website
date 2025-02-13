document.getElementById("encodeBtn").addEventListener("click", encodeImage);
document.getElementById("decodeBtn").addEventListener("click", decodeImage);

async function encodeImage() {
  const imageFile = document.getElementById("imageInput").files[0];
  const message = document.getElementById("messageInput").value;
  
  if (!imageFile || !message) {
    alert("Please select an image and enter a message.");
    return;
  }
  
  const formData = new FormData();
  formData.append("image", imageFile);
  formData.append("message", message);
  
  try {
    const response = await fetch("http://localhost:5000/encode", {
      method: "POST",
      body: formData
    });
    if (!response.ok) throw new Error("Network response was not ok");
    
    // If the API returns an image, we load it on the canvas
    const blob = await response.blob();
    const img = new Image();
    img.onload = function() {
      const canvas = document.getElementById("resultCanvas");
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0);
    }
    img.src = URL.createObjectURL(blob);
    
  } catch (error) {
    console.error("Error encoding image:", error);
    alert("An error occurred while encoding the image.");
  }
}

async function decodeImage() {
  const imageFile = document.getElementById("imageInput").files[0];
  
  if (!imageFile) {
    alert("Please select an image to decode.");
    return;
  }
  
  const formData = new FormData();
  formData.append("image", imageFile);
  
  try {
    const response = await fetch("http://localhost:5000/decode", {
      method: "POST",
      body: formData
    });
    if (!response.ok) throw new Error("Network response was not ok");
    
    const result = await response.json();
    alert("Decoded message: " + result.message);
  } catch (error) {
    console.error("Error decoding image:", error);
    alert("An error occurred while decoding the image.");
  }
}
