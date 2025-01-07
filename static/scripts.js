function uploadFolder() {
  const input = document.getElementById("folderInput");
  const files = input.files;
  const loader = document.getElementById('loader');
  loader.style.display = 'block';

  if (files.length === 0) {
    alert("Please select a folder.");
    return;
  }

  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append("files[]", files[i]);
  }

  fetch("api/upload_folder", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      loader.style.display = 'none';

      displayKenomData(data.identifier_map);
    })
    .catch((error) => console.error("Error:", error));
}

function displayKenomData(identifierMap) {
  const kenomListElement = document.getElementById("kenomList");
  kenomListElement.innerHTML = "";

  for (const [identifier, kenom] of Object.entries(identifierMap)) {
    const option = document.createElement("option");
    option.textContent = kenom; // Display identifier
    option.value = identifier;
    // Store kenom as value
    kenomListElement.appendChild(option);
  }

  kenomListElement.addEventListener("change", function () {
    const selectedKenom = this.value;
    fetchImages(selectedKenom);
  });
}

function fetchImages(identifier) {
  const encodedKenom = encodeURIComponent(identifier);
  const loader = document.getElementById('loader');

  // Show the loader
  loader.style.display = 'block';
  fetch(`/api/get_images/${encodedKenom}`)
    .then((response) => response.json())
    .then((data) => {
      loader.style.display = 'none';
      displayImagesnoraml(data.imgs.imagenormal);
      displayImagesalbedo(data.imgs.imagealbedo);
      displayImageply(data.imgs.mesh);
    })
    .catch((error) => console.error("Error fetching images:", error));
}

function clearply() {
  const plyContainer = document.getElementById("plyContainer");
  plyContainer.innerHTML = "";
}
function fetchcomapare() {

  const loader = document.getElementById('loader');
  loader.style.display = 'block';

  fetch(`/comparefeatures`)
    .then((response) => response.json())
    .then((data) => {
      loader.style.display = 'none';

      console.log(data);
      displaycomparedata(data);
    })
    .catch((error) => console.error("Error fetching images:", error));
}

function displaycomparedata(data) {
  const srimg = document.getElementById("srcimg");
  srimg.innerHTML = data.srcimg;
  const catimg = document.getElementById("catimg1");
  catimg.innerHTML = data.srcimg;
  const nearimg = document.getElementById("nearimg");
  nearimg.innerHTML = data.nearimg;
  const catimgg = document.getElementById("catimg2");
  catimgg.innerHTML = data.nearimg;
  const distance = document.getElementById("distance");
  distance.innerHTML = data.distance;
  const distancem = document.getElementById("distance2");
  distancem.innerHTML = data.distance;
  displareusltimg(data.image);

}
function displareusltimg(image) {
  const selectedImageDiv = document.getElementById("resultimg");
  selectedImageDiv.innerHTML = ""; // Clear previous images


  const imgContainer = document.createElement("div");
  const imgElement = document.createElement("img");


  imgElement.src = image; // Ensure this path matches your Flask static file serving
  imgElement.alt = "Image";

  imgContainer.appendChild(imgElement);
  selectedImageDiv.appendChild(imgContainer);
}

function displayImagesnoraml(image) {
  const selectedImageDiv = document.getElementById("noramlimage");
  selectedImageDiv.innerHTML = ""; // Clear previous images


  const imgContainer = document.createElement("div");
  imgContainer.className = "image-container";
  const imgElement = document.createElement("img");


  imgElement.src = image; // Ensure this path matches your Flask static file serving
  imgElement.alt = "Image";
  imgElement.style.width = "400px";

  imgContainer.appendChild(imgElement);
  selectedImageDiv.appendChild(imgContainer);
}
function displayImagesalbedo(image) {
  const selectedImageDiv = document.getElementById("albeldoimage");
  selectedImageDiv.innerHTML = ""; // Clear previous images


  const imgContainer = document.createElement("div");
  imgContainer.className = "image-container";
  const imgElement = document.createElement("img");

  imgElement.src = image; // Ensure this path matches your Flask static file serving
  imgElement.alt = "Image";
  imgElement.style.width = "400px";

  imgContainer.appendChild(imgElement);
  selectedImageDiv.appendChild(imgContainer);
}
function displayImageply(image) {
  const plyContainer = document.getElementById("plyContainer");
  plyContainer.innerHTML = ""; // Clear previous PLY mesh

  // Create a Three.js scene for the PLY mesh
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(1000, 600);
  plyContainer.appendChild(renderer.domElement);

  // Add lighting
  const light = new THREE.PointLight(0xffffff, 2,100);
  light.position.set(0, 10, 0);
  scene.add(light);

  // Load the PLY file
  const loader = new THREE.PLYLoader();
  loader.load(image, function (geometry) {
    geometry.computeBoundingSphere();
    const material = new THREE.PointsMaterial({ size: 0.2, vertexColors: true });
    const points = new THREE.Points(geometry, material);
    scene.add(points);

    // Set camera position
    camera.position.z = 15;

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.update();
    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      points.rotation.x += 0.0001; // Rotate the mesh
      points.rotation.y += 0.0001;
      renderer.render(scene, camera);
    }
    animate();
  }, undefined, function (error) {
    console.error("An error occurred while loading the PLY file:", error);
  });
}

function previewGrayscale() {
  const methodSelect = document.getElementById("Grayscalemethods");
  const selectedMethod = methodSelect.value;
  const selectedImage = document.querySelector("#selectedimage img"); // Get the currently selected image

  if (!selectedImage) {
    alert("Please select an image first.");
    return;
  }

  // Create a canvas to resize the image
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  const desiredWidth = 300; // Set your desired width
  const desiredHeight = 300; // Set your desired height

  // Set canvas dimensions
  canvas.width = desiredWidth;
  canvas.height = desiredHeight;

  // Create a new image object
  const img = new Image();
  img.crossOrigin = "Anonymous"; // Handle CORS if the image is from a different origin
  img.src = selectedImage.src;

  img.onload = function () {
    // Draw the image on the canvas
    ctx.drawImage(img, 0, 0, desiredWidth, desiredHeight);

    // Get the resized image data URL
    const resizedImageDataUrl = canvas.toDataURL("image/png");

    // Prepare the form data
    const formData = new FormData();
    formData.append("method", selectedMethod);
    formData.append("image", resizedImageDataUrl); // Send the resized image data URL

    // Send the request
    fetch("/preview_grayscale", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.preview_url) {
          const previewDiv = document.getElementById("grayscalePreview");
          previewDiv.innerHTML = `<img src="${data.preview_url}" alt="Grayscale Preview" >`;
        } else {
          alert("Error generating preview.");
        }
      })
      .catch((error) => console.error("Error:", error));
  };

  img.onerror = function () {
    alert("Error loading image.");
  };
}

function extractfeaters() {
  const colormap = document.getElementById('featureSelect').value;
  const loader = document.getElementById('loader');
  loader.style.display = 'block';
  const url = `/extractfeature/${colormap}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      loader.style.display = 'none';
      displayfeaturedata(data);

    })
    .catch((error) => console.error("Error fetching images:", error));


}



function displayfeaturedata(data) {
  const selectedImageDiv = document.getElementById("featerimage");
  selectedImageDiv.innerHTML = ""; // Clear previous images
  const featurediv = document.getElementById("featureshape");
  featurediv.innerHTML = data.features;

  const imgContainer = document.createElement("div");
  imgContainer.className = "image-container";
  const imgElement = document.createElement("img");

  imgElement.src = data.image; // Ensure this path matches your Flask static file serving
  imgElement.alt = "Image";
 

  imgContainer.appendChild(imgElement);
  selectedImageDiv.appendChild(imgContainer);
}


async function finishProcess() {
    try {
        // Send a POST request to the /api/clear_folders endpoint
        const response = await fetch('/api/clear_folders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Check if the request was successful
        if (response.ok) {
            const result = await response.json();
            console.log(result.message); // Log the success message
            alert('All folders cleared successfully!'); // Notify the user
        } else {
            console.error('Failed to clear folders:', response.statusText);
            alert('Failed to clear folders. Please try again.'); // Notify the user of failure
        }
    } catch (error) {
        console.error('Error clearing folders:', error);
        alert('An error occurred while clearing folders.'); // Notify the user of an error
    }
}
document.addEventListener("DOMContentLoaded", function () {
  const steps = document.querySelectorAll(".step");
  const nextBtns = document.querySelectorAll(".next-btn");
  const prevBtns = document.querySelectorAll(".prev-btn");
  let currentStep = 0;
  steps[currentStep].classList.add("active");

  nextBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (currentStep < steps.length - 1) {
        steps[currentStep].classList.remove("active");
        currentStep++;
        steps[currentStep].classList.add("active");
      }
    });
  });

  prevBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (currentStep > 0) {
        steps[currentStep].classList.remove("active");
        currentStep--;
        steps[currentStep].classList.add("active");
      }
    });
  });
});
